from .produto import Produto

class ItemPedido:

    #chama o objeto Produto como atrubuto
    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade

    #exemplos de getters
    @property
    def produto(self) -> Produto:
        return self._produto

    @property
    def quantidade(self) -> int:
        return self._quantidade

    #calcula o subtotal
    @property
    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade
    
    def __str__(self) -> str:
        return f"Item: {self.produto.nome} | Qtd: {self.quantidade} | Subtotal: R$ {self.subtotal:.2f}"