import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

# Imports de Repositories
from repositories.cliente_repository import ClienteRepository
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepository

# Imports de Services e Models
from services.cliente_service import ClienteService
from services.pedido_service import PedidoService
from models.processador_pagamento import ProcessadorPagamento
from models.pedido import Pedido

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Hamburgueria POO - Sistema Visual")
        self.geometry("1000x700")

        # --- 1. Injeção de Dependências ---
        self.cliente_repo = ClienteRepository()
        self.pedido_repo = PedidoRepository()
        self.produto_repo = ProdutoRepository()
        
        self.produto_repo.salvar_padroes_se_vazio()

        self.pagamento_proc = ProcessadorPagamento()
        self.cliente_service = ClienteService(self.cliente_repo)
        self.pedido_service = PedidoService(self.pedido_repo, self.pagamento_proc)

        # Variáveis de Estado
        self.pedido_atual: Pedido = None
        self.cliente_selecionado_obj = None

        # --- 2. Configuração das Abas ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Frames das Abas
        self.frame_clientes = tk.Frame(self.notebook)
        self.frame_pedidos = tk.Frame(self.notebook)
        self.frame_historico = tk.Frame(self.notebook)
        
        self.notebook.add(self.frame_clientes, text="Gestão de Clientes")
        self.notebook.add(self.frame_pedidos, text="Novo Pedido")
        self.notebook.add(self.frame_historico, text="Histórico de Vendas")

        # Setup de cada aba
        self._setup_aba_clientes()
        self._setup_aba_pedidos()
        self._setup_aba_historico()
        
        # Cargas iniciais
        self._atualizar_lista_clientes()
        self._atualizar_combo_clientes()
        self._atualizar_cardapio()
        self._atualizar_historico()

    # =======================================================
    #                   ABA CLIENTES (REFATORADA)
    # =======================================================
    def _setup_aba_clientes(self):
        # Formulário
        lbl_frame_form = ttk.LabelFrame(self.frame_clientes, text="Cadastrar Novo Cliente")
        lbl_frame_form.pack(fill='x', padx=10, pady=5)

        # Linha 0: Nome
        ttk.Label(lbl_frame_form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = ttk.Entry(lbl_frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        # Linha 0: Telefone
        ttk.Label(lbl_frame_form, text="Telefone:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_telefone = ttk.Entry(lbl_frame_form, width=20)
        self.entry_telefone.grid(row=0, column=3, padx=5, pady=5)

        # Linha 1: Cidade (Simplificado)
        ttk.Label(lbl_frame_form, text="Cidade:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_cidade = ttk.Entry(lbl_frame_form, width=30)
        self.entry_cidade.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Botão Salvar
        btn_salvar = ttk.Button(lbl_frame_form, text="Salvar Cliente", command=self._salvar_cliente)
        btn_salvar.grid(row=2, column=0, columnspan=4, pady=10)

        # Listagem
        lbl_frame_lista = ttk.LabelFrame(self.frame_clientes, text="Clientes Cadastrados")
        lbl_frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

        # Ajuste nas colunas: 'endereco' foi substituído por 'cidade'
        colunas = ('id', 'nome', 'telefone', 'cidade')
        self.tree_clientes = ttk.Treeview(lbl_frame_lista, columns=colunas, show='headings')
        self.tree_clientes.heading('id', text='ID')
        self.tree_clientes.heading('nome', text='Nome')
        self.tree_clientes.heading('telefone', text='Telefone')
        self.tree_clientes.heading('cidade', text='Cidade')
        
        self.tree_clientes.column('id', width=40)
        self.tree_clientes.column('nome', width=200)
        self.tree_clientes.column('telefone', width=120)
        self.tree_clientes.column('cidade', width=200)

        scrollbar = ttk.Scrollbar(lbl_frame_lista, orient="vertical", command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscroll=scrollbar.set)
        self.tree_clientes.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _salvar_cliente(self):
        try:
            nome = self.entry_nome.get()
            tel = self.entry_telefone.get()
            cidade = self.entry_cidade.get()
            
            # Validação simples
            if not nome or not tel or not cidade:
                messagebox.showwarning("Aviso", "Todos os campos (Nome, Telefone, Cidade) são obrigatórios!")
                return

            # Chamada ao Service (agora com apenas 3 argumentos)
            self.cliente_service.cadastrar_cliente(nome, tel, cidade)
            
            messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado!")
            
            self._limpar_campos_cliente()
            self._atualizar_lista_clientes()
            self._atualizar_combo_clientes()

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao salvar: {e}")

    def _limpar_campos_cliente(self):
        # Limpa apenas os campos que restaram
        for entry in [self.entry_nome, self.entry_telefone, self.entry_cidade]:
            entry.delete(0, 'end')

    def _atualizar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        self.lista_clientes_cache = self.cliente_service.listar_clientes()
        
        for cli in self.lista_clientes_cache:
            # Exibe a cidade diretamente, sem formatação de endereço complexo
            self.tree_clientes.insert('', 'end', values=(cli.id, cli.nome, cli.telefone, cli.cidade))

    # =======================================================
    #                   ABA PEDIDOS
    # =======================================================
    def _setup_aba_pedidos(self):
        frame_topo = tk.Frame(self.frame_pedidos)
        frame_topo.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_topo, text="Selecione o Cliente:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.combo_clientes = ttk.Combobox(frame_topo, width=50, state="readonly")
        self.combo_clientes.pack(side='left', padx=10)
        self.combo_clientes.bind("<<ComboboxSelected>>", self._on_cliente_selecionado)

        paned = ttk.PanedWindow(self.frame_pedidos, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=5)

        # Cardápio
        frame_cardapio = ttk.LabelFrame(paned, text="Cardápio")
        paned.add(frame_cardapio, weight=1)

        self.tree_cardapio = ttk.Treeview(frame_cardapio, columns=('nome', 'preco', 'tipo'), show='headings')
        self.tree_cardapio.heading('nome', text='Produto')
        self.tree_cardapio.heading('preco', text='Preço')
        self.tree_cardapio.heading('tipo', text='Tipo')
        self.tree_cardapio.column('nome', width=150)
        self.tree_cardapio.column('preco', width=80)
        self.tree_cardapio.column('tipo', width=100)
        self.tree_cardapio.pack(fill='both', expand=True, padx=5, pady=5)

        # Ações
        frame_acoes = tk.Frame(paned)
        paned.add(frame_acoes, weight=0)

        ttk.Label(frame_acoes, text="Qtd:").pack(pady=(50, 5))
        self.entry_qtd = ttk.Entry(frame_acoes, width=5)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(pady=5)

        btn_add = ttk.Button(frame_acoes, text="Adicionar >>", command=self._adicionar_item)
        btn_add.pack(pady=20, padx=10)

        # Carrinho
        frame_carrinho = ttk.LabelFrame(paned, text="Carrinho do Pedido")
        paned.add(frame_carrinho, weight=1)

        self.tree_carrinho = ttk.Treeview(frame_carrinho, columns=('produto', 'qtd', 'subtotal'), show='headings')
        self.tree_carrinho.heading('produto', text='Produto')
        self.tree_carrinho.heading('qtd', text='Qtd')
        self.tree_carrinho.heading('subtotal', text='Subtotal')
        self.tree_carrinho.column('produto', width=150)
        self.tree_carrinho.column('qtd', width=50)
        self.tree_carrinho.column('subtotal', width=80)
        self.tree_carrinho.pack(fill='both', expand=True, padx=5, pady=5)

        # Footer
        frame_footer = tk.Frame(self.frame_pedidos, bg="#f0f0f0")
        frame_footer.pack(fill='x', padx=10, pady=10)

        self.lbl_total = ttk.Label(frame_footer, text="TOTAL: R$ 0.00", font=('Arial', 14, 'bold'), background="#f0f0f0")
        self.lbl_total.pack(side='right', padx=20)

        self.btn_finalizar = ttk.Button(frame_footer, text="Finalizar Pagamento", state="disabled", command=self._abrir_janela_pagamento)
        self.btn_finalizar.pack(side='right')

    def _atualizar_combo_clientes(self):
        self.lista_clientes_cache = self.cliente_service.listar_clientes()
        # Atualizado para mostrar cidade
        valores = [f"{c.nome} ({c.telefone}) - {c.cidade}" for c in self.lista_clientes_cache]
        self.combo_clientes['values'] = valores

    def _atualizar_cardapio(self):
        self.cardapio_cache = self.produto_repo.buscar_todos()
        for item in self.tree_cardapio.get_children():
            self.tree_cardapio.delete(item)
        for i, prod in enumerate(self.cardapio_cache):
            tipo = type(prod).__name__
            self.tree_cardapio.insert('', 'end', iid=i, values=(prod.nome, f"R$ {prod.preco:.2f}", tipo))

    def _on_cliente_selecionado(self, event):
        idx = self.combo_clientes.current()
        if idx >= 0:
            cliente = self.lista_clientes_cache[idx]
            self.cliente_selecionado_obj = cliente
            self.pedido_atual = self.pedido_service.criar_pedido(cliente)
            self._atualizar_carrinho_view()

    def _adicionar_item(self):
        if not self.pedido_atual:
            messagebox.showwarning("Atenção", "Selecione um cliente primeiro.")
            return

        selecionado = self.tree_cardapio.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
        
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade inválida.")
            return

        idx = int(selecionado)
        produto = self.cardapio_cache[idx]
        self.pedido_service.adicionar_item(self.pedido_atual, produto, qtd)
        self._atualizar_carrinho_view()

    def _atualizar_carrinho_view(self):
        for item in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(item)
        
        if not self.pedido_atual:
            self.lbl_total.config(text="TOTAL: R$ 0.00")
            self.btn_finalizar.config(state="disabled")
            return

        for item in self.pedido_atual._itens:
            self.tree_carrinho.insert('', 'end', values=(item.produto.nome, item.quantidade, f"R$ {item.subtotal:.2f}"))
        
        total = self.pedido_atual.total
        self.lbl_total.config(text=f"TOTAL: R$ {total:.2f}")
        
        if total > 0:
            self.btn_finalizar.config(state="normal")
        else:
            self.btn_finalizar.config(state="disabled")

    # =======================================================
    #            LÓGICA DE PAGAMENTO
    # =======================================================

    def _abrir_janela_pagamento(self):
        if not self.pedido_atual or self.pedido_atual.total <= 0:
            return

        janela_pgto = Toplevel(self)
        janela_pgto.title("Finalizar Pedido")
        janela_pgto.geometry("300x200")
        janela_pgto.grab_set() 

        ttk.Label(janela_pgto, text=f"Total a Pagar: R$ {self.pedido_atual.total:.2f}", font=('Arial', 12, 'bold')).pack(pady=20)
        ttk.Label(janela_pgto, text="Escolha a forma de pagamento:").pack(pady=5)

        frame_botoes = tk.Frame(janela_pgto)
        frame_botoes.pack(pady=10)

        ttk.Button(frame_botoes, text="Dinheiro", command=lambda: self._concluir_pagamento("Dinheiro", janela_pgto)).pack(fill='x', pady=2)
        ttk.Button(frame_botoes, text="Cartão", command=lambda: self._concluir_pagamento("Cartão", janela_pgto)).pack(fill='x', pady=2)
        ttk.Button(frame_botoes, text="Pix", command=lambda: self._concluir_pagamento("Pix", janela_pgto)).pack(fill='x', pady=2)

    def _concluir_pagamento(self, forma: str, janela: Toplevel):
        try:
            sucesso = self.pedido_service.finalizar_pedido(self.pedido_atual, forma)
            
            if sucesso:
                janela.destroy() 
                messagebox.showinfo("Sucesso", f"Pagamento via {forma} confirmado!\nPedido Salvo.")
                
                self.pedido_atual = None
                self.combo_clientes.set('')
                self.cliente_selecionado_obj = None
                self._atualizar_carrinho_view()
                
                self._atualizar_historico()
                self.notebook.select(self.frame_historico)
            else:
                messagebox.showerror("Erro", "Falha ao processar pagamento.")
        
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro: {e}")

    # =======================================================
    #            ABA HISTÓRICO
    # =======================================================
    
    def _setup_aba_historico(self):
        btn_refresh = ttk.Button(self.frame_historico, text="🔄 Atualizar Lista", command=self._atualizar_historico)
        btn_refresh.pack(pady=10, padx=10, anchor='e')

        colunas = ('id', 'cliente', 'total', 'status')
        self.tree_historico = ttk.Treeview(self.frame_historico, columns=colunas, show='headings')
        
        self.tree_historico.heading('id', text='ID Pedido')
        self.tree_historico.heading('cliente', text='Cliente')
        self.tree_historico.heading('total', text='Total')
        self.tree_historico.heading('status', text='Status')
        
        self.tree_historico.column('id', width=50, anchor='center')
        self.tree_historico.column('cliente', width=200)
        self.tree_historico.column('total', width=100)
        self.tree_historico.column('status', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(self.frame_historico, orient="vertical", command=self.tree_historico.yview)
        self.tree_historico.configure(yscroll=scrollbar.set)
        
        self.tree_historico.pack(fill='both', expand=True, padx=10, pady=5)
        scrollbar.pack(side='right', fill='y')

    def _atualizar_historico(self):
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
            
        clientes = self.cliente_service.listar_clientes()
        pedidos = self.pedido_service.listar_pedidos(clientes)
        
        for p in pedidos:
            self.tree_historico.insert('', 'end', values=(p.id, p.cliente.nome, f"R$ {p.total:.2f}", p.status))

if __name__ == "__main__":
    from database import init_db
    init_db()
    app = MainWindow()
    app.mainloop()