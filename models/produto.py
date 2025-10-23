from abc import ABC, abstractmethod

#classe mãe abstrata que vai ser usada como molde para os itens do cardápio
class Produto(ABC):

    #usamos _(underline) para atributos protegidos, encapsulamento
    def __init__(self, nome: str, preco: float, desc: str):
        self._nome = nome
        self._preco = preco
        self._descricao = desc

    #exemplos de getters, propriedades de encapsulamento
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def preco(self) -> float:
        return self._preco
    
    @property
    def descricao(self) -> str:
        return self._descricao

    #retorna a representação do produto
    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f}"