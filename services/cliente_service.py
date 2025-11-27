from typing import List, Optional
from models.cliente import Cliente
from models.endereco import Endereco

class ClienteService:

    # Injeção de dependência aqui também
    def __init__(self, repository):
        self.repository = repository

    def cadastrar_cliente(self, nome: str, telefone: str, rua: str, numero: str, bairro: str, cidade: str) -> Optional[Cliente]:
        novo_endereco = Endereco(rua=rua, numero=numero, bairro=bairro, cidade=cidade)
        novo_cliente = Cliente(nome=nome, telefone=telefone, endereco=novo_endereco)

        try:
            return self.repository.salvar(novo_cliente)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"O telefone '{telefone}' já está cadastrado.")
            raise e

    def listar_clientes(self) -> List[Cliente]:
        return self.repository.buscar_todos()