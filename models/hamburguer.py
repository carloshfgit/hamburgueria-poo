from .produto import Produto

class Hamburguer(Produto):

    def __init__(self, nome: str, preco: float, desc: str, ingredientes: list[str]):
        super().__init__(nome, preco, desc)
        self.__ingredientes = ingredientes

    def __str__(self) -> str:
        # Podemos reusar o __str__ da classe pai e adicionar mais informações
        base_str = super().__str__()
        return f"{base_str} (Ingredientes: {', '.join(self.__ingredientes)})"