from typing import List
from database import get_db_connection
from models.produto import Produto
from models.hamburguer import Hamburguer
from models.bebida import Bebida
from models.acompanhamento import Acompanhamento

class ProdutoRepository:

    def buscar_todos(self) -> List[Produto]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        rows = cursor.fetchall()
        conn.close()

        cardapio = []
        for row in rows:
            tipo = row['tipo']
            # Reconstrói o objeto certo baseado no tipo salvo (Polimorfismo na veia!)
            if tipo == 'Hamburguer':
                # Ingredientes salvos como texto "Pão,Carne", convertemos de volta para lista
                ingredientes_list = row['ingredientes'].split(",") if row['ingredientes'] else []
                prod = Hamburguer(row['nome'], row['preco'], row['descricao'], ingredientes_list)
            elif tipo == 'Bebida':
                prod = Bebida(row['nome'], row['preco'], row['descricao'], row['volume_ml'])
            elif tipo == 'Acompanhamento':
                prod = Acompanhamento(row['nome'], row['preco'], row['descricao'], row['tamanho'])
            else:
                continue # Pula tipos desconhecidos
            
            # (Opcional) Se quiser salvar o ID no objeto para uso futuro
            # prod._id = row['id'] 
            cardapio.append(prod)
            
        return cardapio

    def salvar_padroes_se_vazio(self):
        """Popula o banco se estiver vazio, para não começarmos sem cardápio."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT count(*) FROM produtos")
        if cursor.fetchone()[0] == 0:
            print("Populando cardápio inicial no banco...")
            # Inserindo dados iniciais (Seed)
            lista = [
                ('Hamburguer', 'X-Monstro', 25.50, 'Completo', 'Bacon,Ovo,Queijo', None, None),
                ('Bebida', 'Coca-Cola', 8.00, 'Lata', None, 350, None),
                ('Acompanhamento', 'Batata Frita', 12.00, 'Crocante', None, None, 'M')
            ]
            cursor.executemany("""
                INSERT INTO produtos (tipo, nome, preco, descricao, ingredientes, volume_ml, tamanho)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, lista)
            conn.commit()
        conn.close()