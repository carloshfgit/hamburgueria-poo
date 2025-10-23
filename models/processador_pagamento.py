from .pedido import Pedido

class ProcessadorPagamento:

    #simula o processamento de um pagamento
    def processar(self, pedido: Pedido, forma_pagamento: str) -> bool:

        print(f"Iniciando pagamento de R$ {pedido.total:.2f} para o pedido.")
        print(f"Forma de pagamento: {forma_pagamento}")

        print("Pagamento processado com sucesso!")
        
        #muda status do pedido
        pedido.marcar_como_pago()
        
        return True