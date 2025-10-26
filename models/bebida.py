from .produto import Produto

class Bebida(Produto):

    def __init__(self, nome:str, preco: float, desc: str, volume_ml: int):
        #chama os atributos da classe mãe e adiciona o atributo específico
        super().__init__(nome, preco, desc)
        self._volume_ml = volume_ml

    def __str__(self) -> str:
        return f"{super().__str__()} - {self._volume_ml}ml"