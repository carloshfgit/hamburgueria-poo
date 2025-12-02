#LÓGICA DE DATABASE | SQL
#transforma os objetos python em comandos SQL para persistência no banco

from typing import List
from models.cliente import Cliente
from database import get_db_connection

class ClienteRepository:

    def salvar(self, cliente: Cliente) -> Cliente:
        """Salva um novo cliente diretamente com a cidade na tabela clientes."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO clientes (nome, telefone, cidade) VALUES (?, ?, ?)",
            (cliente.nome, cliente.telefone, cliente.cidade)
        )
        
        cliente._id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        print(f"Repositório: Cliente '{cliente.nome}' salvo com ID {cliente.id}.")
        return cliente

    def buscar_todos(self) -> List[Cliente]:
        """Carrega todos os clientes de forma simples (sem JOIN)."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, telefone, cidade FROM clientes")
        
        clientes = []
        for row in cursor.fetchall():

            cliente = Cliente(
                id=row['id'],
                nome=row['nome'],
                telefone=row['telefone'],
                cidade=row['cidade']
            )
            clientes.append(cliente)
            
        conn.close()
        return clientes