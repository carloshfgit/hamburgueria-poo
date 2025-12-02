class Cliente:

    def __init__(self, nome: str, telefone: str, cidade: str, id: int = None):
        self._id = id
        self._nome = nome
        self._telefone = telefone
        self._cidade = cidade

    #exemplos de getters, propriedades de encapsulamento
    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def telefone(self) -> str:
        return self._telefone
    
    @property
    def cidade(self) -> str:
        return self._cidade

    def __str__(self) -> str:
        return f"Cliente: {self.nome}, Tel: {self.telefone}\nCidade: {self.cidade}"