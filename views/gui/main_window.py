#CONTROLADOR DA LÓGICA DE ITERAÇÃO DA INTERFACE GRÁFICA
#controla e faz a comunicação entre as abas, orquetrador de eventos

import tkinter as tk
from tkinter import ttk

from database import init_db
from repositories.cliente_repository import ClienteRepository
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepository
from services.cliente_service import ClienteService
from services.pedido_service import PedidoService
from models.processador_pagamento import ProcessadorPagamento

from views.gui.abas.aba_clientes import AbaClientes
from views.gui.abas.aba_pedidos import AbaPedidos
from views.gui.abas.aba_historico import AbaHistorico

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Hamburgueria POO - Sistema Modular")
        self.geometry("1000x700")

        #Injeção de dependencias
        # criamos todos os repositórios e serviços aqui e passamos
        # para as abas. Nenhuma aba cria conexão com banco sozinha.
        
        self.cliente_repo = ClienteRepository()
        self.pedido_repo = PedidoRepository()
        self.produto_repo = ProdutoRepository()
        
        #garante cardápio inicial se banco estiver vazio
        self.produto_repo.salvar_padroes_se_vazio()

        self.pagamento_proc = ProcessadorPagamento()
        
        self.cliente_service = ClienteService(self.cliente_repo)
        self.pedido_service = PedidoService(self.pedido_repo, self.pagamento_proc)

        #configuração visual
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        #instanciando as abas
        
        #aba de clientes
        self.aba_clientes = AbaClientes(
            parent=self.notebook, 
            service=self.cliente_service
        )

        #aba de pedidos
        self.aba_pedidos = AbaPedidos(
            parent=self.notebook,
            service_pedido=self.pedido_service,
            service_cliente=self.cliente_service,
            repo_produto=self.produto_repo,
            on_pedido_salvo_callback=self._ao_finalizar_pedido
        )

        #aba de historico
        self.aba_historico = AbaHistorico(
            parent=self.notebook,
            service_pedido=self.pedido_service,
            service_cliente=self.cliente_service
        )

        #adiciona tudo ao notebook
        self.notebook.add(self.aba_clientes, text="Gestão de Clientes")
        self.notebook.add(self.aba_pedidos, text="Novo Pedido")
        self.notebook.add(self.aba_historico, text="Histórico de Vendas")
        self.notebook.bind("<<NotebookTabChanged>>", self._ao_mudar_aba)

    def _ao_finalizar_pedido(self):
        """
        Método chamado automaticamente pela AbaPedidos quando
        um pagamento é concluído com sucesso.
        """
        print("Callback recebido: Pedido finalizado.")
        self.aba_historico.atualizar_historico()
        self.notebook.select(self.aba_historico)

    def _ao_mudar_aba(self, event):
        """
        Sempre que mudar de aba,forçar atualizações
        para garantir que os dados estejam frescos.
        """
        aba_selecionada = self.notebook.select()
        widget_aba = self.notebook.nametowidget(aba_selecionada)

        if widget_aba == self.aba_pedidos:
            
            self.aba_pedidos.atualizar_combo_clientes()
            
        elif widget_aba == self.aba_historico:
            self.aba_historico.atualizar_historico()

if __name__ == "__main__":
    init_db()
    app = MainWindow()
    app.mainloop()