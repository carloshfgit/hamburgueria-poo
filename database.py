import sqlite3
from typing import List, Dict
from models.cliente import Cliente
from models.endereco import Endereco
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.produto import Produto

DATABASE_URL = "hamburgueria.db"

#cria e retorna uma conexão com o banco de dados.
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    #isso faz com que os resultados venham como dicionários (melhor para mapear)
    conn.row_factory = sqlite3.Row 
    return conn

#cria as tabelas do banco de dados se elas não existirem.
def init_db():
    
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

    #aqui começamos a implementar as funções

#FUNÇÕES DE CLIENTES
def salvar_cliente(cliente: Cliente) -> Cliente:
    """Salva um novo cliente e seu endereço no DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    #salvando o endereço
    end = cliente.endereco
    cursor.execute(
        "INSERT INTO enderecos (rua, numero, bairro, cidade) VALUES (?, ?, ?, ?)",
        (end.rua, end.numero, end.bairro, end.cidade)
    )
    endereco_id = cursor.lastrowid
    #atualiza o id
    end._id = endereco_id 
    
    #salvando cliente com o id do endereço
    cursor.execute(
        "INSERT INTO clientes (nome, telefone, endereco_id) VALUES (?, ?, ?)",
        (cliente.nome, cliente.telefone, endereco_id)
    )
    cliente_id = cursor.lastrowid
    #atualiza id do cliente
    cliente._id = cliente_id
    
    conn.commit()
    conn.close()
    
    print(f"Cliente '{cliente.nome}' (ID: {cliente.id}) salvo.")
    return cliente

#carrega todos os clientes e seus endereços do DB
def carregar_clientes() -> List[Cliente]:
    
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


#FUNÇÕES DE PEDIDOS
def salvar_pedido(pedido: Pedido) -> Pedido:
    """Salva um novo pedido e seus itens no DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    #salvando o pedido principal
    cursor.execute(
        "INSERT INTO pedidos (cliente_id, status, total) VALUES (?, ?, ?)",
        (pedido.cliente.id, pedido.status, pedido.total)
    )
    pedido_id = cursor.lastrowid
    pedido._id = pedido_id #atualiza o id do pedido
    
    #salvando os itens do pedido
    for item in pedido._itens:
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_nome, produto_preco, quantidade) VALUES (?, ?, ?, ?)",
            (pedido_id, item.produto.nome, item.produto.preco, item.quantidade)
        )
        
    conn.commit()
    conn.close()
    print(f"Pedido ID: {pedido.id} salvo.")
    return pedido

#atualiza o status do pedido
def atualizar_status_pedido(pedido: Pedido):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (pedido.status, pedido.id)
    )
    
    conn.commit()
    conn.close()
    print(f"Status do Pedido ID: {pedido.id} atualizado para '{pedido.status}'.")

#carrega todos os pedidos e seus itens do DB
def carregar_pedidos(clientes: List[Cliente]) -> List[Pedido]:
    
    #criando um mapa de id
    clientes_map: Dict[int, Cliente] = {c.id: c for c in clientes}
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    #carregando os pedidos
    cursor.execute("SELECT * FROM pedidos ORDER BY id")
    pedidos_rows = cursor.fetchall()
    
    pedidos_map: Dict[int, Pedido] = {}
    
    for row in pedidos_rows:
        cliente_obj = clientes_map.get(row['cliente_id'])
        if not cliente_obj:
            print(f"Aviso: Cliente ID {row['cliente_id']} não encontrado para o Pedido ID {row['id']}.")
            continue
            
        pedido = Pedido(cliente=cliente_obj, id=row['id'])
        pedido._status = row['status'] #atualiza o status
        pedidos_map[pedido.id] = pedido

    #carrega todos os itens e os associa aos pedidos
    cursor.execute("SELECT * FROM itens_pedido")
    itens_rows = cursor.fetchall()
    
    for item_row in itens_rows:
        pedido = pedidos_map.get(item_row['pedido_id'])
        if pedido:
            #recria um objeto "Produto" genérico com os dados salvos
            #isso é suficiente para calcular total e exibir o nome
            produto_db = Produto(
                nome=item_row['produto_nome'],
                preco=item_row['produto_preco'],
                desc="" 
            )
            item_db = ItemPedido(produto=produto_db, quantidade=item_row['quantidade'])
            pedido._itens.append(item_db)
            
    conn.close()
    
    lista_pedidos = list(pedidos_map.values())
    print(f"Carregados {len(lista_pedidos)} pedidos.")
    return lista_pedidos