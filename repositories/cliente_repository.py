from typing import List
from models.cliente import Cliente
# A importação de Endereco foi removida pois a classe não é mais usada aqui
from database import get_db_connection

class ClienteRepository:

    def salvar(self, cliente: Cliente) -> Cliente:
        """Salva um novo cliente diretamente com a cidade na tabela clientes."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Mudança Principal: Inserção direta (sem criar endereço antes)
        cursor.execute(
            "INSERT INTO clientes (nome, telefone, cidade) VALUES (?, ?, ?)",
            (cliente.nome, cliente.telefone, cliente.cidade)
        )
        
        # Recupera o ID gerado automaticamente pelo banco
        cliente._id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        print(f"Repositório: Cliente '{cliente.nome}' salvo com ID {cliente.id}.")
        return cliente

    def buscar_todos(self) -> List[Cliente]:
        """Carrega todos os clientes de forma simples (sem JOIN)."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Mudança Principal: SELECT simples, sem JOIN com tabela de endereços
        cursor.execute("SELECT id, nome, telefone, cidade FROM clientes")
        
        clientes = []
        for row in cursor.fetchall():
            # Instancia o Cliente passando a string 'cidade' diretamente
            # Certifique-se que seu __init__ no model espera (nome, telefone, cidade, id)
            cliente = Cliente(
                id=row['id'],
                nome=row['nome'],
                telefone=row['telefone'],
                cidade=row['cidade']
            )
            clientes.append(cliente)
            
        conn.close()
        return clientes