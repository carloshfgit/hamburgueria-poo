# Arquivo: models/endereco.py

class Endereco:

    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
        self._rua = rua
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade

    # <<< MUDANÇA: Propriedades (Getters) para encapsulamento >>>
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
        # <<< MUDANÇA: Usando as próprias propriedades (boa prática) >>>
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}"