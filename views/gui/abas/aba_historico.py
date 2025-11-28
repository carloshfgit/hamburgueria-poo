import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

class AbaHistorico(tk.Frame):
    def __init__(self, parent, service_pedido, service_cliente):
        """
        :param parent: Widget pai (Notebook)
        :param service_pedido: Instância de PedidoService
        :param service_cliente: Instância de ClienteService (necessário para listar nomes nos pedidos)
        """
        super().__init__(parent)
        self.service_pedido = service_pedido
        self.service_cliente = service_cliente
        
        # Cache local para armazenar os objetos de pedido listados na tela
        self.pedidos_cache = []

        self._setup_ui()
        self.atualizar_historico()

    def _setup_ui(self):
        # Frame de topo para Botões de Ação
        frame_acoes = tk.Frame(self)
        frame_acoes.pack(fill='x', padx=10, pady=5)

        btn_refresh = ttk.Button(frame_acoes, text="🔄 Atualizar", command=self.atualizar_historico)
        btn_refresh.pack(side='right', padx=5)

        # Botões de Ação
        btn_detalhes = ttk.Button(frame_acoes, text="📄 Ver Itens", command=self._ver_detalhes_pedido)
        btn_detalhes.pack(side='left', padx=5)

        btn_cancelar = ttk.Button(frame_acoes, text="🚫 Cancelar Pedido", command=self._cancelar_pedido_gui)
        btn_cancelar.pack(side='left', padx=5)

        # Tabela (Treeview)
        colunas = ('id', 'cliente', 'total', 'status')
        self.tree_historico = ttk.Treeview(self, columns=colunas, show='headings')
        
        self.tree_historico.heading('id', text='ID')
        self.tree_historico.heading('cliente', text='Cliente')
        self.tree_historico.heading('total', text='Total')
        self.tree_historico.heading('status', text='Status')
        
        self.tree_historico.column('id', width=50, anchor='center')
        self.tree_historico.column('cliente', width=200)
        self.tree_historico.column('total', width=100)
        self.tree_historico.column('status', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_historico.yview)
        self.tree_historico.configure(yscroll=scrollbar.set)
        
        self.tree_historico.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Bind para duplo clique
        self.tree_historico.bind("<Double-1>", lambda e: self._ver_detalhes_pedido())

    def atualizar_historico(self):
        # Limpa a visualização atual
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
            
        # Busca clientes atualizados para garantir nomes corretos
        clientes = self.service_cliente.listar_clientes()
        
        # Busca pedidos através do serviço injetado
        self.pedidos_cache = self.service_pedido.listar_pedidos(clientes)
        
        for p in self.pedidos_cache:
            # Usamos o iid=p.id para facilitar a recuperação do objeto depois
            self.tree_historico.insert('', 'end', iid=p.id, values=(p.id, p.cliente.nome, f"R$ {p.total:.2f}", p.status))

    def _ver_detalhes_pedido(self):
        selecionado_id = self.tree_historico.focus() 
        if not selecionado_id:
            return
        
        # Busca o objeto pedido no cache local usando o ID (que é o iid da treeview)
        pedido_obj = next((p for p in self.pedidos_cache if str(p.id) == selecionado_id), None)
        
        if not pedido_obj:
            return

        # Cria Janela Pop-up (Modal)
        janela_det = Toplevel(self)
        janela_det.title(f"Itens do Pedido #{pedido_obj.id}")
        janela_det.geometry("400x300")
        
        ttk.Label(janela_det, text=f"Cliente: {pedido_obj.cliente.nome}", font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Lista simples dos itens
        tree_itens = ttk.Treeview(janela_det, columns=('prod', 'qtd', 'sub'), show='headings')
        tree_itens.heading('prod', text='Produto')
        tree_itens.heading('qtd', text='Qtd')
        tree_itens.heading('sub', text='Subtotal')
        
        tree_itens.column('prod', width=200)
        tree_itens.column('qtd', width=50, anchor='center')
        tree_itens.column('sub', width=80)
        
        tree_itens.pack(fill='both', expand=True, padx=10, pady=5)
        
        for item in pedido_obj._itens:
            tree_itens.insert('', 'end', values=(item.produto.nome, item.quantidade, f"R$ {item.subtotal:.2f}"))
            
        ttk.Label(janela_det, text=f"Total Pago: R$ {pedido_obj.total:.2f}", font=('Arial', 11, 'bold')).pack(pady=10)

    def _cancelar_pedido_gui(self):
        selecionado_id = self.tree_historico.focus()
        if not selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um pedido para cancelar.")
            return

        pedido_obj = next((p for p in self.pedidos_cache if str(p.id) == selecionado_id), None)
        
        if not pedido_obj:
            return
            
        if pedido_obj.status == "Cancelado":
            messagebox.showinfo("Info", "Este pedido já está cancelado.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"Deseja cancelar o pedido #{pedido_obj.id} de {pedido_obj.cliente.nome}?")
        if confirmar:
            # Chama o serviço para cancelar
            msg_resultado = self.service_pedido.cancelar_pedido(pedido_obj)
            
            if msg_resultado == "sucesso":
                messagebox.showinfo("Sucesso", "Pedido cancelado com sucesso!")
            elif msg_resultado == "cancelado_pago":
                messagebox.showinfo("Sucesso", "Pedido PAGO foi estornado e cancelado.")
            else:
                messagebox.showinfo("Aviso", "Pedido já estava cancelado.")
            
            # Atualiza a lista para refletir o novo status
            self.atualizar_historico()