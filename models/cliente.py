from .endereco import Endereco

class Cliente:

    #usa o objeto endereço como atributo de cliente
    def __init__(self, nome: str, telefone: str, endereco: Endereco):
        self._nome = nome
        self._telefone = telefone
        self._endereco = endereco

    #exemplos de getters, propriedades de encapsulamento
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def telefone(self) -> str:
        return self._telefone

    @property
    def endereco(self) -> Endereco:
        return self._endereco

    def __str__(self) -> str:
        return f"Cliente: {self.nome}, Tel: {self.telefone}\nEndereço: {self.endereco}"