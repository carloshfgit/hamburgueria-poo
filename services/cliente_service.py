from typing import List, Optional
from models.cliente import Cliente
# A importação de 'models.endereco' foi removida pois não é mais usada

class ClienteService:

    def __init__(self, repository):
        self.repository = repository

    # Assinatura simplificada: recebe apenas nome, telefone e cidade
    def cadastrar_cliente(self, nome: str, telefone: str, cidade: str) -> Optional[Cliente]:
        
        # Agora instanciamos o Cliente passando a cidade diretamente
        # Isso assume que você já alterou o __init__ do model Cliente na etapa 2
        novo_cliente = Cliente(nome=nome, telefone=telefone, cidade=cidade)

        try:
            return self.repository.salvar(novo_cliente)
        except Exception as e:
            # Mantemos a validação de telefone único que já existia
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"O telefone '{telefone}' já está cadastrado.")
            raise e

    def listar_clientes(self) -> List[Cliente]:
        return self.repository.buscar_todos()