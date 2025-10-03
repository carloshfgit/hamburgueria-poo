from abc import ABC, abstractmethod

class Produto(ABC):

    def __init__(self, nome: str, preco: float, desc: str):
        self._nome = nome
        self._preco = preco
        self._descricao = desc

    def get_preco(self) -> float:
        return self._preco
    
    def __str__(self) -> str:
        return f"{self._nome} - R$ {self._preco:.2f}"