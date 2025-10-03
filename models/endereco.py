class Endereco:

    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
        self.__rua = rua
        self.__numero = numero
        self.__bairro = bairro
        self.__cidade = cidade

    def __str__(self) -> str:
        return f"{self._rua}, {self._numero} - {self._bairro}, {self._cidade}"