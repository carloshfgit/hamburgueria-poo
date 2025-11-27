from typing import List
from models.pedido import Pedido
from models.produto import Produto
from models.cliente import Cliente
# Removemos as importações concretas das classes Repository e ProcessadorPagamento aqui
# para evitar dependência direta, mas mantemos a tipagem se quiser (opcional)

class PedidoService:

    # Agora injetamos as dependências no construtor
    def __init__(self, repository, processador_pagamento):
        self.repository = repository
        self.processador_pagamento = processador_pagamento

    def criar_pedido(self, cliente: Cliente) -> Pedido:
        """Inicia um pedido vazio para um cliente."""
        return Pedido(cliente=cliente)

    def adicionar_item(self, pedido: Pedido, produto: Produto, quantidade: int):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        pedido.adicionar_item(produto, quantidade)

    def finalizar_pedido(self, pedido: Pedido, forma_pagamento: str) -> bool:
        # Usa o processador injetado
        pagamento_ok = self.processador_pagamento.processar(pedido, forma_pagamento)

        if pagamento_ok:
            self.repository.salvar(pedido)
            return True
        return False

    def cancelar_pedido(self, pedido: Pedido) -> str:
        resultado = pedido.cancelar()
        if resultado in ["sucesso", "cancelado_pago"]:
            self.repository.atualizar_status(pedido)
        return resultado

    def listar_pedidos(self, lista_clientes: List[Cliente]) -> List[Pedido]:
        return self.repository.buscar_todos(lista_clientes)