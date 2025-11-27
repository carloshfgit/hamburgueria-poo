from typing import List
from models.cliente import Cliente
from models.endereco import Endereco
from database import get_db_connection

class ClienteRepository:

    def salvar(self, cliente: Cliente) -> Cliente:
        """Salva um novo cliente e seu endereço no banco."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Salvar endereço
        end = cliente.endereco
        cursor.execute(
            "INSERT INTO enderecos (rua, numero, bairro, cidade) VALUES (?, ?, ?, ?)",
            (end.rua, end.numero, end.bairro, end.cidade)
        )
        # Recupera o ID gerado para o endereço
        end._id = cursor.lastrowid 
        
        # 2. Salvar cliente usando o ID do endereço
        cursor.execute(
            "INSERT INTO clientes (nome, telefone, endereco_id) VALUES (?, ?, ?)",
            (cliente.nome, cliente.telefone, end.id)
        )
        # Recupera o ID gerado para o cliente
        cliente._id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        print(f"Repositório: Cliente '{cliente.nome}' salvo com ID {cliente.id}.")
        return cliente

    def buscar_todos(self) -> List[Cliente]:
        """Carrega todos os clientes e seus endereços."""
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
        return clientes