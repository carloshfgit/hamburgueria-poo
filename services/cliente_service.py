from typing import List, Optional
from models.cliente import Cliente
from models.endereco import Endereco
from repositories.cliente_repository import ClienteRepository

class ClienteService:

    def __init__(self):
        self.repository = ClienteRepository()

    def cadastrar_cliente(self, nome: str, telefone: str, rua: str, numero: str, bairro: str, cidade: str) -> Optional[Cliente]:
        """
        Cria as instâncias de Endereco e Cliente e tenta salvar no banco.
        Retorna o Cliente se der certo, ou lança uma exceção se der erro.
        """
        # Regra de Negócio: Criar os objetos
        novo_endereco = Endereco(rua=rua, numero=numero, bairro=bairro, cidade=cidade)
        novo_cliente = Cliente(nome=nome, telefone=telefone, endereco=novo_endereco)

        try:
            # Chama a camada de dados
            return self.repository.salvar(novo_cliente)
        except Exception as e:
            # Aqui poderíamos criar exceções personalizadas, 
            # mas por enquanto vamos apenas repassar o erro ou tratar o básico
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"O telefone '{telefone}' já está cadastrado.")
            raise e

    def listar_clientes(self) -> List[Cliente]:
        return self.repository.buscar_todos()