from.produto import Produto

class Acompanhamento(Produto):

    def __init__(self, nome: str, preco: float, desc: str, tamanho: str):
        #chama os atributos da classe mãe e adiciona o atributo específico
        super().__init__(nome, preco, desc)
        self._tamanho = tamanho

    def __str__(self) -> str:
        return f"{super().__str__()} (Tamanho: {self._tamanho})"