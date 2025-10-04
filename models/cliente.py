from .endereco import Endereco

class Cliente:

    def __init__(self, nome: str, telefone: str, endereco: Endereco):
        self._nome = nome
        self._telefone = telefone
        self._endereco = endereco

    def __str__(self) -> str:
        return f"Cliente: {self._nome}, Tel: {self._telefone}\nEndereço: {self._endereco}"