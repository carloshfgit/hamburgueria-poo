from .cliente import Cliente
from .item_pedido import ItemPedido
from .produto import Produto
from typing import List

class Pedido:

    #associa Pedido a Cliente, chamando o objeto Cliente como atributo
    def __init__(self, cliente: Cliente):
        self._cliente = cliente
        self._itens: List[ItemPedido] = []
        self._status: str = "Recebido"

    #aqui temos exemplos de Getters
    #permite que o app.py leia o status sem acessar o atributo privado
    @property
    def status(self) -> str:
        return self._status
    
    #permite que o app.py leia o cliente sem acessar o atributo privado
    @property
    def cliente(self) -> Cliente:
        return self._cliente

    #aplicando polimorfismo de subtipos (inclusão), produto pode ser Bebida, Hamburguer, Acompanhamento
    def adicionar_item(self, produto: Produto, quantidade: int):
        novo_item = ItemPedido(produto, quantidade)
        self._itens.append(novo_item)
       
    #calcula o total usando o subtotal(de item_pedido) e o transforma em atributo virtual
    @property
    def total(self) -> float:
        if not self._itens:
            return 0.0
        return sum(item.subtotal for item in self._itens)

    #método para cancelamento de pedido
    def cancelar(self) -> str:
        
        if self._status == "Cancelado":
            return "ja_cancelado"
        
        if self._status == "Pago":
            self._status = "Cancelado"
            return "cancelado_pago"

        self._status = "Cancelado"
        return "sucesso"

    #representa o pedido final e suas informações, depois de adicionado todos os itens desejados
    def __str__(self) -> str:
        itens_str = "\n".join(map(str, self._itens))
        return (
            f"--- Pedido ---\n"
            f"{self.cliente}\n" 
            f"Status: {self.status}\n" # <<< MUDANÇA: Usa self.status
            f"--- Itens ---\n"
            f"{itens_str}\n"
            f"----------------\n"
            f"TOTAL DO PEDIDO: R$ {self.total:.2f}\n"
            f"----------------"
        )
    
    def marcar_como_pago(self):
        """
        Altera o status do pedido para 'Pago'.
        Este método é a interface pública para permitir que 
        outras classes (como o ProcessadorPagamento) 
        informem ao pedido que ele foi pago.
        """
        #a própria classe Pedido é responsável por mudar seu estado.
        self._status = "Pago"