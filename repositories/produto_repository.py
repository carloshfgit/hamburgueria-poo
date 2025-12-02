#LÓGICA DE DATABASE | SQL
#transforma os objetos python em comandos SQL para persistência no banco

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
        
            if tipo == 'Hamburguer':
                ingredientes_list = row['ingredientes'].split(",") if row['ingredientes'] else []
                prod = Hamburguer(row['nome'], row['preco'], row['descricao'], ingredientes_list)
            elif tipo == 'Bebida':
                prod = Bebida(row['nome'], row['preco'], row['descricao'], row['volume_ml'])
            elif tipo == 'Acompanhamento':
                prod = Acompanhamento(row['nome'], row['preco'], row['descricao'], row['tamanho'])
            else:
                continue 
        
            cardapio.append(prod)
            
        return cardapio

    def salvar_padroes_se_vazio(self):
        """Popula o banco se estiver vazio, para não começarmos sem cardápio."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT count(*) FROM produtos")
        if cursor.fetchone()[0] == 0:
            print("Populando cardápio inicial no banco...")
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