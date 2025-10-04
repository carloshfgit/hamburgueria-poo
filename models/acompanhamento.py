from.produto import Produto

class Acompanhamento(Produto):

    def __init__(self, nome: str, preco: float, desc: str, tamanho: str):
        super().__init__(nome, preco, desc)
        self._tamanho = tamanho

    def __str__(self) -> str:
        return f"{super().__str__()} (Tamanho: {self._tamanho})"