import sqlite3

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