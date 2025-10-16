from abc import ABC, abstractmethod

#classe mãe abstrata que vai ser usada como molde para os itens do cardápio
class Produto(ABC):

    def __init__(self, nome: str, preco: float, desc: str):
        self._nome = nome
        self._preco = preco
        self._descricao = desc

    #garante encapsulamento, retorna o preço protegido do produto em vez de acessáço diretamente
    def get_preco(self) -> float:
        return self._preco
    
    def __str__(self) -> str:
        return f"{self._nome} - R$ {self._preco:.2f}"