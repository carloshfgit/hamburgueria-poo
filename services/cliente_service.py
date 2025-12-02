#APLICA REGRAS DE NEGÓCIO
#recebe os dados e envia objetos prontos para o repositório
from typing import List, Optional
from models.cliente import Cliente

class ClienteService:

    def __init__(self, repository):
        self.repository = repository

    def cadastrar_cliente(self, nome: str, telefone: str, cidade: str) -> Optional[Cliente]:
        
        novo_cliente = Cliente(nome=nome, telefone=telefone, cidade=cidade)

        try:
            return self.repository.salvar(novo_cliente)
        except Exception as e:

            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"O telefone '{telefone}' já está cadastrado.")
            raise e

    def listar_clientes(self) -> List[Cliente]:
        return self.repository.buscar_todos()
    
    