import tkinter as tk
from tkinter import ttk

# --- 1. Imports de Infraestrutura e Domínio ---
from database import init_db
from repositories.cliente_repository import ClienteRepository
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepository
from services.cliente_service import ClienteService
from services.pedido_service import PedidoService
from models.processador_pagamento import ProcessadorPagamento

# --- 2. Imports das Novas Abas (Views) ---
# Certifique-se de que criou o arquivo __init__.py dentro da pasta 'abas'
from views.gui.abas.aba_clientes import AbaClientes
from views.gui.abas.aba_pedidos import AbaPedidos
from views.gui.abas.aba_historico import AbaHistorico

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Hamburgueria POO - Sistema Modular")
        self.geometry("1000x700")

        # =======================================================
        #           INJEÇÃO DE DEPENDÊNCIAS (SETUP)
        # =======================================================
        # Criamos todos os repositórios e serviços aqui e passamos
        # para as abas. Nenhuma aba cria conexão com banco sozinha.
        
        self.cliente_repo = ClienteRepository()
        self.pedido_repo = PedidoRepository()
        self.produto_repo = ProdutoRepository()
        
        # Garante cardápio inicial se banco estiver vazio
        self.produto_repo.salvar_padroes_se_vazio()

        self.pagamento_proc = ProcessadorPagamento()
        
        self.cliente_service = ClienteService(self.cliente_repo)
        self.pedido_service = PedidoService(self.pedido_repo, self.pagamento_proc)

        # =======================================================
        #           CONFIGURAÇÃO VISUAL (LAYOUT)
        # =======================================================
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Instanciação das Abas ---
        
        # 1. Aba Clientes
        self.aba_clientes = AbaClientes(
            parent=self.notebook, 
            service=self.cliente_service
        )

        # 2. Aba Pedidos
        # Passamos um callback 'on_pedido_salvo_callback'
        # Quando o pedido terminar, executará self._ao_finalizar_pedido
        self.aba_pedidos = AbaPedidos(
            parent=self.notebook,
            service_pedido=self.pedido_service,
            service_cliente=self.cliente_service,
            repo_produto=self.produto_repo,
            on_pedido_salvo_callback=self._ao_finalizar_pedido
        )

        # 3. Aba Histórico
        self.aba_historico = AbaHistorico(
            parent=self.notebook,
            service_pedido=self.pedido_service,
            service_cliente=self.cliente_service
        )

        # Adiciona as instâncias ao Notebook
        self.notebook.add(self.aba_clientes, text="Gestão de Clientes")
        self.notebook.add(self.aba_pedidos, text="Novo Pedido")
        self.notebook.add(self.aba_historico, text="Histórico de Vendas")
        
        # Define binds globais se necessário (ex: atualizar listas ao mudar de aba)
        self.notebook.bind("<<NotebookTabChanged>>", self._ao_mudar_aba)

    def _ao_finalizar_pedido(self):
        """
        Método chamado automaticamente pela AbaPedidos quando
        um pagamento é concluído com sucesso.
        """
        print("Callback recebido: Pedido finalizado.")
        
        # 1. Atualiza a lista do histórico para mostrar o novo pedido
        self.aba_historico.atualizar_historico()
        
        # 2. Foca na aba de histórico
        self.notebook.select(self.aba_historico)

    def _ao_mudar_aba(self, event):
        """
        Opcional: Sempre que mudar de aba, podemos forçar atualizações
        para garantir que os dados estejam frescos.
        """
        aba_selecionada = self.notebook.select()
        widget_aba = self.notebook.nametowidget(aba_selecionada)

        if widget_aba == self.aba_pedidos:
            # Se for para pedidos, recarrega clientes (caso tenha cadastrado um novo)
            self.aba_pedidos.atualizar_combo_clientes()
            
        elif widget_aba == self.aba_historico:
            self.aba_historico.atualizar_historico()

if __name__ == "__main__":
    init_db()
    app = MainWindow()
    app.mainloop()