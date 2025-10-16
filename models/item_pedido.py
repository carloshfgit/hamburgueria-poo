from .produto import Produto

class ItemPedido:

    #chama o objeto Produto como atrubuto
    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade

    #transforma o metodo subtotal em um atributo virtual
    @property
    def subtotal(self) -> float:
        return self._produto.get_preco() * self._quantidade
    
    def __str__(self) -> str:
        return f"Item: {self._produto._nome} | Qtd: {self._quantidade} | Subtotal: R$ {self.subtotal:.2f}"