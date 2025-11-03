# hamburgueria_poo/database.py

import sqlite3
from typing import List, Dict

# Importe seus modelos
from models.cliente import Cliente
from models.endereco import Endereco
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.produto import Produto # Precisamos disto para recriar os itens

DATABASE_URL = "hamburgueria.db"

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_URL)
    # Isso faz com que os resultados venham como dicionários (melhor para mapear)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Cria as tabelas do banco de dados se elas não existirem."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela para Endereços
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enderecos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rua TEXT NOT NULL,
        numero TEXT,
        bairro TEXT NOT NULL,
        cidade TEXT NOT NULL
    )
    """)
    
    # Tabela para Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL UNIQUE,
        endereco_id INTEGER NOT NULL,
        FOREIGN KEY (endereco_id) REFERENCES enderecos (id)
    )
    """)
    
    # Tabela para Pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
    """)
    
    # Tabela para Itens de um Pedido
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto_nome TEXT NOT NULL,
        produto_preco REAL NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("Banco de dados inicializado.")

    # --- Funções de Cliente ---

def salvar_cliente(cliente: Cliente) -> Cliente:
    """Salva um novo cliente e seu endereço no DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Salvar o Endereço primeiro
    end = cliente.endereco
    cursor.execute(
        "INSERT INTO enderecos (rua, numero, bairro, cidade) VALUES (?, ?, ?, ?)",
        (end.rua, end.numero, end.bairro, end.cidade)
    )
    endereco_id = cursor.lastrowid
    # Atualiza o ID no objeto
    end._id = endereco_id 
    
    # 2. Salvar o Cliente com o ID do endereço
    cursor.execute(
        "INSERT INTO clientes (nome, telefone, endereco_id) VALUES (?, ?, ?)",
        (cliente.nome, cliente.telefone, endereco_id)
    )
    cliente_id = cursor.lastrowid
    # Atualiza o ID no objeto
    cliente._id = cliente_id
    
    conn.commit()
    conn.close()
    
    print(f"Cliente '{cliente.nome}' (ID: {cliente.id}) salvo.")
    return cliente

def carregar_clientes() -> List[Cliente]:
    """Carrega todos os clientes e seus endereços do DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id as cliente_id, c.nome, c.telefone,
               e.id as endereco_id, e.rua, e.numero, e.bairro, e.cidade
        FROM clientes c
        JOIN enderecos e ON c.endereco_id = e.id
    """)
    
    clientes = []
    for row in cursor.fetchall():
        endereco = Endereco(
            id=row['endereco_id'],
            rua=row['rua'],
            numero=row['numero'],
            bairro=row['bairro'],
            cidade=row['cidade']
        )
        cliente = Cliente(
            id=row['cliente_id'],
            nome=row['nome'],
            telefone=row['telefone'],
            endereco=endereco
        )
        clientes.append(cliente)
        
    conn.close()
    print(f"Carregados {len(clientes)} clientes.")
    return clientes

# --- Funções de Pedido ---

def salvar_pedido(pedido: Pedido) -> Pedido:
    """Salva um novo pedido e seus itens no DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Salvar o Pedido principal
    cursor.execute(
        "INSERT INTO pedidos (cliente_id, status, total) VALUES (?, ?, ?)",
        (pedido.cliente.id, pedido.status, pedido.total)
    )
    pedido_id = cursor.lastrowid
    pedido._id = pedido_id # Atualiza o ID no objeto
    
    # 2. Salvar os Itens do Pedido
    for item in pedido._itens: # Acessando o atributo privado (idealmente teria um getter)
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_nome, produto_preco, quantidade) VALUES (?, ?, ?, ?)",
            (pedido_id, item.produto.nome, item.produto.preco, item.quantidade)
        )
        
    conn.commit()
    conn.close()
    print(f"Pedido ID: {pedido.id} salvo.")
    return pedido

def atualizar_status_pedido(pedido: Pedido):
    """Atualiza o status de um pedido existente (ex: para 'Cancelado')."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (pedido.status, pedido.id)
    )
    
    conn.commit()
    conn.close()
    print(f"Status do Pedido ID: {pedido.id} atualizado para '{pedido.status}'.")

def carregar_pedidos(clientes: List[Cliente]) -> List[Pedido]:
    """Carrega todos os pedidos e seus itens do DB."""
    
    # Cria um mapa de ID -> Objeto Cliente para fácil acesso
    clientes_map: Dict[int, Cliente] = {c.id: c for c in clientes}
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Carregar todos os pedidos
    cursor.execute("SELECT * FROM pedidos ORDER BY id")
    pedidos_rows = cursor.fetchall()
    
    pedidos_map: Dict[int, Pedido] = {}
    
    for row in pedidos_rows:
        cliente_obj = clientes_map.get(row['cliente_id'])
        if not cliente_obj:
            print(f"Aviso: Cliente ID {row['cliente_id']} não encontrado para o Pedido ID {row['id']}.")
            continue
            
        pedido = Pedido(cliente=cliente_obj, id=row['id'])
        pedido._status = row['status'] # Atualiza o status
        pedidos_map[pedido.id] = pedido

    # 2. Carregar todos os itens e associá-los aos pedidos
    cursor.execute("SELECT * FROM itens_pedido")
    itens_rows = cursor.fetchall()
    
    for item_row in itens_rows:
        pedido = pedidos_map.get(item_row['pedido_id'])
        if pedido:
            # Recria um objeto "Produto" genérico com os dados salvos
            # Isso é suficiente para calcular total e exibir o nome
            produto_db = Produto(
                nome=item_row['produto_nome'],
                preco=item_row['produto_preco'],
                desc="" # Descrição não foi salva, mas não é crítica
            )
            item_db = ItemPedido(produto=produto_db, quantidade=item_row['quantidade'])
            pedido._itens.append(item_db)
            
    conn.close()
    
    lista_pedidos = list(pedidos_map.values())
    print(f"Carregados {len(lista_pedidos)} pedidos.")
    return lista_pedidos