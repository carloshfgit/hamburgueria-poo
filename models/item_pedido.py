# Arquivo: models/item_pedido.py

from .produto import Produto

class ItemPedido:

    #chama o objeto Produto como atrubuto
    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade

    # <<< MUDANÇA: Propriedades (Getters) para consistência >>>
    @property
    def produto(self) -> Produto:
        return self._produto

    @property
    def quantidade(self) -> int:
        return self._quantidade

    #transforma o metodo subtotal em um atributo virtual
    @property
    def subtotal(self) -> float:
        # <<< MUDANÇA: Usa as propriedades de ItemPedido e (futuras) de Produto >>>
        # Isso assume que Produto terá uma propriedade .preco
        return self.produto.preco * self.quantidade
    
    def __str__(self) -> str:
        # <<< MUDANÇA: Usa as propriedades de ItemPedido e (futuras) de Produto >>>
        # Isso assume que Produto terá uma propriedade .nome
        return f"Item: {self.produto.nome} | Qtd: {self.quantidade} | Subtotal: R$ {self.subtotal:.2f}"