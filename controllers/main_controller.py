from services.cliente_service import ClienteService
from services.pedido_service import PedidoService
from views.console_view import ConsoleView
from models.hamburguer import Hamburguer # Apenas para carregar cardapio fake
from models.bebida import Bebida

class MainController:

    def __init__(self):
        self.cliente_service = ClienteService()
        self.pedido_service = PedidoService()
        self.view = ConsoleView()
        
        # Simulando cardapio (idealmente viria de um ProdutoService/Repository)
        self.cardapio = self._carregar_cardapio_fake()

    def iniciar(self):
        while True:
            opcao = self.view.exibir_menu_principal()
            
            if opcao == '1':
                self._fluxo_criar_pedido()
            elif opcao == '2':
                self._fluxo_cadastrar_cliente()
            elif opcao == '3':
                pedidos = self.pedido_service.listar_pedidos(self.cliente_service.listar_clientes())
                self.view.listar_pedidos(pedidos)
                self.view.pausar()
            elif opcao == '4':
                clientes = self.cliente_service.listar_clientes()
                self.view.listar_clientes(clientes)
                self.view.pausar()
            elif opcao == '5':
                self._fluxo_cancelar_pedido()
            elif opcao == '0':
                self.view.mostrar_mensagem("Saindo...")
                break
            else:
                self.view.mostrar_mensagem("Opção inválida!")

    def _fluxo_cadastrar_cliente(self):
        dados = self.view.obter_dados_cliente()
        try:
            cliente = self.cliente_service.cadastrar_cliente(
                nome=dados['nome'], 
                telefone=dados['telefone'],
                rua=dados['rua'],
                numero=dados['numero'],
                bairro=dados['bairro'],
                cidade=dados['cidade']
            )
            self.view.mostrar_mensagem(f"Cliente {cliente.nome} cadastrado com sucesso!")
        except Exception as e:
            self.view.mostrar_mensagem(f"Erro: {e}")
        self.view.pausar()

    def _fluxo_criar_pedido(self):
        # 1. Identificar Cliente
        clientes = self.cliente_service.listar_clientes()
        cliente_selecionado = self.view.selecionar_cliente(clientes)
        
        if cliente_selecionado == 'N':
            self._fluxo_cadastrar_cliente()
            return # Retorna para o menu para tentar de novo
        
        if not cliente_selecionado:
            return

        # 2. Criar Pedido
        pedido = self.pedido_service.criar_pedido(cliente_selecionado)
        
        # 3. Loop de Produtos
        while True:
            produto = self.view.selecionar_produto(self.cardapio)
            if not produto:
                break
            
            qtd = self.view.pedir_quantidade()
            if qtd > 0:
                self.pedido_service.adicionar_item(pedido, produto, qtd)
                self.view.mostrar_mensagem(f"Item adicionado! Subtotal: R${pedido.total:.2f}")

        if pedido.total == 0:
            self.view.mostrar_mensagem("Pedido vazio cancelado.")
            return

        # 4. Pagamento
        self.view.mostrar_resumo_pedido(pedido)
        forma_pgto = self.view.obter_forma_pagamento()
        
        sucesso = self.pedido_service.finalizar_pedido(pedido, forma_pgto)
        if sucesso:
            self.view.mostrar_mensagem("✅ Pedido finalizado e salvo!")
        else:
            self.view.mostrar_mensagem("❌ Falha no pagamento.")
        self.view.pausar()

    def _fluxo_cancelar_pedido(self):
        # Carregar pedidos
        clientes = self.cliente_service.listar_clientes()
        pedidos = self.pedido_service.listar_pedidos(clientes)
        
        pedido = self.view.selecionar_pedido_cancelamento(pedidos)
        if pedido:
            resultado = self.pedido_service.cancelar_pedido(pedido)
            self.view.mostrar_mensagem(f"Resultado do cancelamento: {resultado}")
        self.view.pausar()

    def _carregar_cardapio_fake(self):
        # Mantive hardcoded como no seu original, mas encapsulado aqui
        return [
            Hamburguer("X-Monstro", 25.50, "Completo", ["Bacon", "Ovo"]),
            Bebida("Coca-Cola", 8.00, "Lata", 350)
        ]