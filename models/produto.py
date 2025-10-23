# Arquivo: models/produto.py

from abc import ABC, abstractmethod

#classe mãe abstrata que vai ser usada como molde para os itens do cardápio
class Produto(ABC):

    #usamos _(underline) para atributos protegidos, encapsulamento
    def __init__(self, nome: str, preco: float, desc: str):
        self._nome = nome
        self._preco = preco
        self._descricao = desc

    # <<< MUDANÇA: "Getters" (Propriedades) para encapsulamento >>>
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def preco(self) -> float:
        return self._preco
    
    @property
    def descricao(self) -> str:
        return self._descricao

    # <<< MUDANÇA: Método get_preco() removido >>>
    # O método abaixo não é mais necessário, pois foi substituído pela @property preco
    # def get_preco(self) -> float:
    #     return self._preco
    
    def __str__(self) -> str:
        # <<< MUDANÇA: Usando as próprias propriedades (boa prática) >>>
        return f"{self.nome} - R$ {self.preco:.2f}"