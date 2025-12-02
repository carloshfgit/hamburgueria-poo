#ESSE ARQUIVO CONTROLA A TELA DE PEDIDOS
#esta é a aba mais complexa, onde ocorre a venda, ela gerencia o fluxo de criar um pedido do zero
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from models.pedido import Pedido

class AbaPedidos(tk.Frame):
    def __init__(self, parent, service_pedido, service_cliente, repo_produto, on_pedido_salvo_callback=None):
        """
        :param parent: Widget pai (Notebook)
        :param service_pedido: Lógica de pedidos
        :param service_cliente: Para listar clientes no combobox
        :param repo_produto: Para buscar o cardápio
        :param on_pedido_salvo_callback: Função para chamar quando um pedido for finalizado com sucesso
        """
        super().__init__(parent)
        self.service_pedido = service_pedido
        self.service_cliente = service_cliente
        self.repo_produto = repo_produto
        self.on_pedido_salvo_callback = on_pedido_salvo_callback

        self.pedido_atual: Pedido = None
        self.cliente_selecionado_obj = None
        self.lista_clientes_cache = []
        self.cardapio_cache = []

        #levanta a tela
        self._setup_ui()
        
        #carrega dados iniciais
        self.atualizar_combo_clientes()
        self.atualizar_cardapio()

    def _setup_ui(self):
        #seleção de cliente
        frame_topo = tk.Frame(self)
        frame_topo.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_topo, text="Selecione o Cliente:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.combo_clientes = ttk.Combobox(frame_topo, width=50, state="readonly")
        self.combo_clientes.pack(side='left', padx=10)
        self.combo_clientes.bind("<<ComboboxSelected>>", self._on_cliente_selecionado)

        paned = ttk.PanedWindow(self, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=5)

        #cardapio
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

        #ações
        frame_acoes = tk.Frame(paned)
        paned.add(frame_acoes, weight=0)

        ttk.Label(frame_acoes, text="Qtd:").pack(pady=(50, 5))
        self.entry_qtd = ttk.Entry(frame_acoes, width=5)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(pady=5)

        btn_add = ttk.Button(frame_acoes, text="Adicionar >>", command=self._adicionar_item)
        btn_add.pack(pady=20, padx=10)

        #carrinho
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

        #total e botao finalizar
        frame_footer = tk.Frame(self, bg="#f0f0f0")
        frame_footer.pack(fill='x', padx=10, pady=10)

        self.lbl_total = ttk.Label(frame_footer, text="TOTAL: R$ 0.00", font=('Arial', 14, 'bold'), background="#f0f0f0")
        self.lbl_total.pack(side='right', padx=20)

        self.btn_finalizar = ttk.Button(frame_footer, text="Finalizar Pagamento", state="disabled", command=self._abrir_janela_pagamento)
        self.btn_finalizar.pack(side='right')

    #logica de carregamento de dados
    def atualizar_combo_clientes(self):
        
        self.lista_clientes_cache = self.service_cliente.listar_clientes()
        valores = [f"{c.nome} ({c.telefone}) - {c.cidade}" for c in self.lista_clientes_cache]
        self.combo_clientes['values'] = valores
        
        self.combo_clientes.set('')
        self.pedido_atual = None
        self._atualizar_carrinho_view()

    def atualizar_cardapio(self):
        self.cardapio_cache = self.repo_produto.buscar_todos()
        for item in self.tree_cardapio.get_children():
            self.tree_cardapio.delete(item)
        for i, prod in enumerate(self.cardapio_cache):
            tipo = type(prod).__name__
            self.tree_cardapio.insert('', 'end', iid=i, values=(prod.nome, f"R$ {prod.preco:.2f}", tipo))

    #eventos de interaçao
    def _on_cliente_selecionado(self, event):
        idx = self.combo_clientes.current()
        if idx >= 0:
            cliente = self.lista_clientes_cache[idx]
            self.cliente_selecionado_obj = cliente
            self.pedido_atual = self.service_pedido.criar_pedido(cliente)
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
        
        # Delega ao service a adição do item
        self.service_pedido.adicionar_item(self.pedido_atual, produto, qtd)
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

    #pagamento
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

        #gorma de pagamento
        ttk.Button(frame_botoes, text="Dinheiro", command=lambda: self._concluir_pagamento("Dinheiro", janela_pgto)).pack(fill='x', pady=2)
        ttk.Button(frame_botoes, text="Cartão", command=lambda: self._concluir_pagamento("Cartão", janela_pgto)).pack(fill='x', pady=2)
        ttk.Button(frame_botoes, text="Pix", command=lambda: self._concluir_pagamento("Pix", janela_pgto)).pack(fill='x', pady=2)

    def _concluir_pagamento(self, forma: str, janela: Toplevel):
        try:
            sucesso = self.service_pedido.finalizar_pedido(self.pedido_atual, forma)
            
            if sucesso:
                janela.destroy() 
                messagebox.showinfo("Sucesso", f"Pagamento via {forma} confirmado!\nPedido Salvo.")
                
                self.pedido_atual = None
                self.combo_clientes.set('')
                self.cliente_selecionado_obj = None
                self._atualizar_carrinho_view()
                
                if self.on_pedido_salvo_callback:
                    self.on_pedido_salvo_callback()
            else:
                messagebox.showerror("Erro", "Falha ao processar pagamento.")
        
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Erro: {e}")