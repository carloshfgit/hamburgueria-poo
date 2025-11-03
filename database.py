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