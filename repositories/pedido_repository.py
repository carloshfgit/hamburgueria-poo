#LÓGICA DE DATABASE | SQL
#transforma os objetos python em comandos SQL para persistência no banco

from typing import List, Dict
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.produto import Produto
from models.cliente import Cliente
from database import get_db_connection
from models.hamburguer import Hamburguer
from models.bebida import Bebida
from models.acompanhamento import Acompanhamento

class PedidoRepository:

    def salvar(self, pedido: Pedido) -> Pedido:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, status, total) VALUES (?, ?, ?)",
            (pedido.cliente.id, pedido.status, pedido.total)
        )
        pedido._id = cursor.lastrowid
        
        # Salva os itens com polimorfismo
        for item in pedido._itens:
            prod = item.produto
            tipo = ""
            detalhes = ""
            
            # Lógica para extrair os detalhes baseada na classe
            if isinstance(prod, Hamburguer):
                tipo = "Hamburguer"
                # Salva ingredientes como string separada por vírgula
                detalhes = ",".join(prod._ingredientes) 
            elif isinstance(prod, Bebida):
                tipo = "Bebida"
                detalhes = str(prod._volume_ml)
            elif isinstance(prod, Acompanhamento):
                tipo = "Acompanhamento"
                detalhes = prod._tamanho
            else:
                tipo = "Produto" # Fallback
            
            cursor.execute("""
                INSERT INTO itens_pedido 
                (pedido_id, produto_nome, produto_preco, produto_tipo, produto_detalhes, quantidade) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (pedido.id, prod.nome, prod.preco, tipo, detalhes, item.quantidade))
            
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
                nome = item_row['produto_nome']
                preco = item_row['produto_preco']
                tipo = item_row['produto_tipo']
                detalhes = item_row['produto_detalhes']
                
                produto_recuperado = None
                
                # Reconstrói o objeto correto
                if tipo == "Hamburguer":
                    ingredientes = detalhes.split(",") if detalhes else []
                    produto_recuperado = Hamburguer(nome, preco, "Histórico", ingredientes)
                elif tipo == "Bebida":
                    volume = int(detalhes) if detalhes else 0
                    produto_recuperado = Bebida(nome, preco, "Histórico", volume)
                elif tipo == "Acompanhamento":
                    produto_recuperado = Acompanhamento(nome, preco, "Histórico", detalhes)
                else:
                    # Fallback genérico se for algo antigo ou desconhecido
                    produto_recuperado = Produto(nome, preco, "Histórico")

                # Adiciona ao pedido
                # Nota: precisamos passar o objeto Produto real agora!
                item_obj = ItemPedido(produto=produto_recuperado, quantidade=item_row['quantidade'])
                pedido._itens.append(item_obj)
                
        conn.close()
        return list(pedidos_map.values())