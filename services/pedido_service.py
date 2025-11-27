from typing import List
from models.pedido import Pedido
from models.produto import Produto
from models.cliente import Cliente
from models.processador_pagamento import ProcessadorPagamento
from repositories.pedido_repository import PedidoRepository

class PedidoService:

    def __init__(self):
        self.repository = PedidoRepository()
        self.processador_pagamento = ProcessadorPagamento()

    def criar_pedido(self, cliente: Cliente) -> Pedido:
        """Inicia um pedido vazio para um cliente."""
        return Pedido(cliente=cliente)

    def adicionar_item(self, pedido: Pedido, produto: Produto, quantidade: int):
        """Adiciona item ao pedido com validação básica."""
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        
        pedido.adicionar_item(produto, quantidade)

    def finalizar_pedido(self, pedido: Pedido, forma_pagamento: str) -> bool:
        """
        Processa o pagamento e, se aprovado, salva o pedido no banco.
        """
        # 1. Processar Pagamento
        pagamento_ok = self.processador_pagamento.processar(pedido, forma_pagamento)

        if pagamento_ok:
            # 2. Salvar no Banco (Persistência)
            self.repository.salvar(pedido)
            return True
        
        return False

    def cancelar_pedido(self, pedido: Pedido) -> str:
        """Tenta cancelar e atualiza o status no banco se necessário."""
        resultado = pedido.cancelar()
        
        if resultado in ["sucesso", "cancelado_pago"]:
            self.repository.atualizar_status(pedido)
            
        return resultado

    def listar_pedidos(self, lista_clientes: List[Cliente]) -> List[Pedido]:
        return self.repository.buscar_todos(lista_clientes)