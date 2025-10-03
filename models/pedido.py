from .cliente import Cliente
from .item_pedido import ItemPedido
from .produto import Produto
from typing import List

class Pedido:

    def __init__(self, cliente: Cliente):
        self._cliente = cliente
        self._itens: List[ItemPedido] = []
        self.status: str = "Recebido"

    def adicionar_item(self, produto: Produto, quantidade: int):
        #aplicando polimorfismo
        novo_item = ItemPedido(produto, quantidade)
        self._itens.append(novo_item)
        print(f"Item '{produto._nome}' adicionado ao pedido.")

    @property
    def total(self) -> float:
        if not self._itens:
            return 0.0
        return sum(item.subtotal for item in self._itens)

    def __str__(self) -> str:
        itens_str = "\n".join(map(str, self._itens))
        return (
            f"--- Pedido ---\n"
            f"{self._cliente}\n"
            f"Status: {self._status}\n"
            f"--- Itens ---\n"
            f"{itens_str}\n"
            f"----------------\n"
            f"TOTAL DO PEDIDO: R$ {self.total:.2f}\n"
            f"----------------"
        )