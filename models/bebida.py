from .produto import Produto

class Bebida(Produto):

    def __init__(self, nome:str, preco: float, desc: str, volume_ml: int):
        super().__init__(nome, preco, desc)
        self.__volume_ml = volume_ml

    