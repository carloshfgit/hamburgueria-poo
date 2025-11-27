from typing import List, Dict
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.produto import Produto
from models.cliente import Cliente
from database import get_db_connection

class PedidoRepository:

    def salvar(self, pedido: Pedido) -> Pedido:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Salva o pedido
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, status, total) VALUES (?, ?, ?)",
            (pedido.cliente.id, pedido.status, pedido.total)
        )
        pedido._id = cursor.lastrowid
        
        # Salva os itens
        for item in pedido._itens:
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_nome, produto_preco, quantidade) VALUES (?, ?, ?, ?)",
                (pedido.id, item.produto.nome, item.produto.preco, item.quantidade)
            )
            
        conn.commit()
        conn.close()
        print(f"Repositório: Pedido ID {pedido.id} salvo.")
        return pedido

    def atualizar_status(self, pedido: Pedido):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE pedidos SET status = ? WHERE id = ?",
            (pedido.status, pedido.id)
        )
        
        conn.commit()
        conn.close()

    def buscar_todos(self, clientes: List[Cliente]) -> List[Pedido]:
        # Cria mapa para busca rápida de clientes por ID
        clientes_map = {c.id: c for c in clientes}
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Busca pedidos
        cursor.execute("SELECT * FROM pedidos ORDER BY id")
        pedidos_rows = cursor.fetchall()
        
        pedidos_map = {}
        
        for row in pedidos_rows:
            cliente = clientes_map.get(row['cliente_id'])
            if not cliente:
                continue
                
            pedido = Pedido(cliente=cliente, id=row['id'])
            pedido._status = row['status']
            pedidos_map[pedido.id] = pedido

        # Busca itens e associa aos pedidos
        cursor.execute("SELECT * FROM itens_pedido")
        itens_rows = cursor.fetchall()
        
        for item_row in itens_rows:
            pedido = pedidos_map.get(item_row['pedido_id'])
            if pedido:
                produto_dummy = Produto(
                    nome=item_row['produto_nome'],
                    preco=item_row['produto_preco'],
                    desc="" 
                )
                item = ItemPedido(produto=produto_dummy, quantidade=item_row['quantidade'])
                pedido._itens.append(item)
                
        conn.close()
        return list(pedidos_map.values())