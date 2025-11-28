from services.cliente_service import ClienteService
from services.pedido_service import PedidoService
from repositories.cliente_repository import ClienteRepository
from repositories.pedido_repository import PedidoRepository
from models.processador_pagamento import ProcessadorPagamento
from views.console.console_view import ConsoleView
from repositories.produto_repository import ProdutoRepository

class MainController:

    def __init__(self):
        self.cliente_repo = ClienteRepository()
        self.pedido_repo = PedidoRepository()
        self.produto_repo = ProdutoRepository() 

        self.pagamento_proc = ProcessadorPagamento()
        
        self.cliente_service = ClienteService(self.cliente_repo)
        self.pedido_service = PedidoService(self.pedido_repo, self.pagamento_proc)
        
        self.view = ConsoleView()
        
        self.produto_repo.salvar_padroes_se_vazio()
        self.cardapio = self.produto_repo.buscar_todos()

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
            # Chamada simplificada: Apenas Nome, Telefone e Cidade
            cliente = self.cliente_service.cadastrar_cliente(
                nome=dados['nome'], 
                telefone=dados['telefone'],
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
            return 
        
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
        clientes = self.cliente_service.listar_clientes()
        pedidos = self.pedido_service.listar_pedidos(clientes)
        
        pedido = self.view.selecionar_pedido_cancelamento(pedidos)
        if pedido:
            resultado = self.pedido_service.cancelar_pedido(pedido)
            self.view.mostrar_mensagem(f"Resultado do cancelamento: {resultado}")
        self.view.pausar()