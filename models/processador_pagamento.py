# Arquivo: models/processador_pagamento.py (Refatorado)

from .pedido import Pedido

class ProcessadorPagamento:

    #simula o processamento de um pagamento, e retorna true se concluído e false se falhar
    def processar(self, pedido: Pedido, forma_pagamento: str) -> bool:
        # Estas linhas usam a propriedade .total, o que está correto!
        print(f"Iniciando pagamento de R$ {pedido.total:.2f} para o pedido.")
        print(f"Forma de pagamento: {forma_pagamento}")
        
        # ... (aqui poderia ter uma lógica real de pagamento) ...
        
        print("Pagamento processado com sucesso!")
        
        # <<< MUDANÇA: Delegação da responsabilidade >>>
        # Em vez de: pedido._status = "Pago"
        # Nós "avisamos" o pedido para que ele mesmo mude seu status.
        pedido.marcar_como_pago()
        
        return True