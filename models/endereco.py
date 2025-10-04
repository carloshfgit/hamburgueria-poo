class Endereco:

    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
        self._rua = rua
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade

    def __str__(self) -> str:
        return f"{self._rua}, {self._numero} - {self._bairro}, {self._cidade}"