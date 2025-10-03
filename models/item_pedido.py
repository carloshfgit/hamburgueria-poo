from .produto import Produto

class ItemPedido:

    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade

    @property
    def subtotal(self) -> float:
        return self._produto.get_preco() * self._quantidade
    
    def __str__(self) -> str:
        return f"Item: {self._produto._nome} | Qtd: {self._quantidade} | Subtotal: R$ {self.subtotal:.2f}"