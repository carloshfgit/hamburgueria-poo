from .produto import Produto

class Hamburguer(Produto):

    def __init__(self, nome: str, preco: float, desc: str, ingredientes: list[str]):
        #chama os atributos da classe mãe e adiciona o atributo específico
        super().__init__(nome, preco, desc)
        self._ingredientes = ingredientes

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} (Ingredientes: {', '.join(self._ingredientes)})"