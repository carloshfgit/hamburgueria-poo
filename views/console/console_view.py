#INTERFACE PURA
#apenas entrada e saída, sem lógica complexa de fluxo
from typing import List, Dict, Any
from models.cliente import Cliente
from models.pedido import Pedido
from models.produto import Produto

class ConsoleView:

    def mostrar_mensagem(self, msg: str):
        print(f"\n{msg}")
    
    def pausar(self):
        input("\nPressione Enter para continuar...")

    def exibir_menu_principal(self) -> str:
        print("\n--- 🍔 Hamburgueria POO - Sistema do Caixa 🍔 ---")
        print("1. Criar Novo Pedido")
        print("2. Cadastrar Novo Cliente")
        print("3. Listar Pedidos (Histórico)")
        print("4. Listar Clientes Cadastrados")
        print("5. Cancelar Pedido")
        print("0. Sair do Sistema")
        return input("Escolha uma opção: ").strip()
    
    def obter_dados_cliente(self) -> Dict[str, str]:
        """Coleta dados simplificados do usuário."""
        print("\n--- Cadastro de Novo Cliente ---")
        dados = {}
        dados['nome'] = input("Nome do cliente: ")
        dados['telefone'] = input("Telefone (ex: 11987654321): ")
        dados['cidade'] = input("Cidade: ")
        return dados

    def listar_clientes(self, clientes: List[Cliente]):
        print("\n--- Clientes Cadastrados ---")
        if not clientes:
            print("Nenhum cliente encontrado.")
            return

        for i, cliente in enumerate(clientes):
            print(f"{i + 1}. {cliente.nome} ({cliente.telefone}) - {cliente.cidade}")

    def selecionar_cliente(self, clientes: List[Cliente]) -> Any:
        self.listar_clientes(clientes)
        print("-------------------------")
        print("N. Cadastrar NOVO cliente")
        
        escolha = input("Digite o número do cliente ou 'N' para novo: ").strip().upper()
        if escolha == 'N':
            return 'N'
        
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(clientes):
                return clientes[idx]
        except ValueError:
            pass
        return None

    def selecionar_produto(self, cardapio: List[Produto]) -> Any:
        print("\n--- Cardápio ---")
        for i, prod in enumerate(cardapio):
            print(f"{i + 1}. {prod.nome} - R${prod.preco:.2f}")
        print("0. Finalizar Seleção")
        
        escolha = input("Escolha o item: ")
        if escolha == '0': 
            return None
            
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(cardapio):
                return cardapio[idx]
        except ValueError:
            print("Opção inválida.")
        return None
    
    def pedir_quantidade(self) -> int:
        try:
            return int(input("Quantidade: "))
        except ValueError:
            return 0

    def mostrar_resumo_pedido(self, pedido: Pedido):
        print(f"\n{pedido}") 

    def obter_forma_pagamento(self) -> str:
        return input("Forma de pagamento (Dinheiro/Cartão/Pix): ")

    def listar_pedidos(self, pedidos: List[Pedido]):
        print("\n--- Histórico de Pedidos ---")
        for p in pedidos:
            print(f"Pedido #{p.id} - {p.cliente.nome} - Total: R${p.total:.2f} - Status: {p.status}")

    def selecionar_pedido_cancelamento(self, pedidos: List[Pedido]) -> Any:
        self.listar_pedidos(pedidos)
        try:
            id_input = int(input("\nDigite o ID do pedido para cancelar (ou 0 para voltar): "))
            if id_input == 0: return None
            for p in pedidos:
                if p.id == id_input:
                    return p
        except ValueError:
            pass
        return None