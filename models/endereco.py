class Endereco:

    def __init__(self, rua: str, numero: str, bairro: str, cidade: str, id: int = None):
        self._id = id
        self._rua = rua
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade

    #getters para encapsulamento
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def rua(self) -> str:
        return self._rua

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def bairro(self) -> str:
        return self._bairro

    @property
    def cidade(self) -> str:
        return self._cidade

    def __str__(self) -> str:
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}"