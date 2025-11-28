import tkinter as tk
from tkinter import ttk, messagebox

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
        self.geometry("1000x700") # Aumentei um pouco para caber o pedido

        # --- 1. Injeção de Dependências ---
        # Repositories
        self.cliente_repo = ClienteRepository()
        self.pedido_repo = PedidoRepository()
        self.produto_repo = ProdutoRepository()
        
        # Garante que o cardápio exista (Seed)
        self.produto_repo.salvar_padroes_se_vazio()

        # Services
        self.pagamento_proc = ProcessadorPagamento()
        self.cliente_service = ClienteService(self.cliente_repo)
        self.pedido_service = PedidoService(self.pedido_repo, self.pagamento_proc)

        # Estado da Aplicação (Variáveis de memória)
        self.pedido_atual: Pedido = None
        self.cliente_selecionado_obj = None

        # --- 2. Configuração das Abas ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Criando os frames das abas
        self.frame_clientes = tk.Frame(self.notebook)
        self.frame_pedidos = tk.Frame(self.notebook)
        
        self.notebook.add(self.frame_clientes, text="Gestão de Clientes")
        self.notebook.add(self.frame_pedidos, text="Novo Pedido")

        # Configura o conteúdo de cada aba
        self._setup_aba_clientes()
        self._setup_aba_pedidos()
        
        # Carrega dados iniciais
        self._atualizar_lista_clientes()
        self._atualizar_combo_clientes() # Novo
        self._atualizar_cardapio()       # Novo

    # =======================================================
    #                   ABA CLIENTES
    # =======================================================
    def _setup_aba_clientes(self):
        # ... (Mesmo código da Fase 1, mantido aqui para integridade) ...
        # Painel de Formulário
        lbl_frame_form = ttk.LabelFrame(self.frame_clientes, text="Cadastrar Novo Cliente")
        lbl_frame_form.pack(fill='x', padx=10, pady=5)

        ttk.Label(lbl_frame_form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = ttk.Entry(lbl_frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(lbl_frame_form, text="Telefone:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_telefone = ttk.Entry(lbl_frame_form, width=20)
        self.entry_telefone.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(lbl_frame_form, text="Rua:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_rua = ttk.Entry(lbl_frame_form, width=25)
        self.entry_rua.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(lbl_frame_form, text="Nº:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.entry_numero = ttk.Entry(lbl_frame_form, width=10)
        self.entry_numero.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(lbl_frame_form, text="Bairro:").grid(row=1, column=4, padx=5, pady=5, sticky='e')
        self.entry_bairro = ttk.Entry(lbl_frame_form, width=20)
        self.entry_bairro.grid(row=1, column=5, padx=5, pady=5)
        
        ttk.Label(lbl_frame_form, text="Cidade:").grid(row=1, column=6, padx=5, pady=5, sticky='e')
        self.entry_cidade = ttk.Entry(lbl_frame_form, width=20)
        self.entry_cidade.grid(row=1, column=7, padx=5, pady=5)

        btn_salvar = ttk.Button(lbl_frame_form, text="Salvar Cliente", command=self._salvar_cliente)
        btn_salvar.grid(row=2, column=0, columnspan=8, pady=10)

        # Painel de Listagem
        lbl_frame_lista = ttk.LabelFrame(self.frame_clientes, text="Clientes Cadastrados")
        lbl_frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

        colunas = ('id', 'nome', 'telefone', 'endereco')
        self.tree_clientes = ttk.Treeview(lbl_frame_lista, columns=colunas, show='headings')
        self.tree_clientes.heading('id', text='ID')
        self.tree_clientes.heading('nome', text='Nome')
        self.tree_clientes.heading('telefone', text='Telefone')
        self.tree_clientes.heading('endereco', text='Endereço')
        
        self.tree_clientes.column('id', width=40)
        self.tree_clientes.column('nome', width=200)
        self.tree_clientes.column('telefone', width=120)
        self.tree_clientes.column('endereco', width=400)

        scrollbar = ttk.Scrollbar(lbl_frame_lista, orient="vertical", command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscroll=scrollbar.set)
        self.tree_clientes.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _salvar_cliente(self):
        try:
            nome = self.entry_nome.get()
            tel = self.entry_telefone.get()
            rua = self.entry_rua.get()
            num = self.entry_numero.get()
            bairro = self.entry_bairro.get()
            cidade = self.entry_cidade.get()

            if not nome or not tel:
                messagebox.showwarning("Aviso", "Nome e Telefone são obrigatórios!")
                return

            self.cliente_service.cadastrar_cliente(nome, tel, rua, num, bairro, cidade)
            messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado!")
            
            self._limpar_campos_cliente()
            self._atualizar_lista_clientes()
            self._atualizar_combo_clientes() # Atualiza também na aba de pedidos!

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao salvar: {e}")

    def _limpar_campos_cliente(self):
        for entry in [self.entry_nome, self.entry_telefone, self.entry_rua, self.entry_numero, self.entry_bairro, self.entry_cidade]:
            entry.delete(0, 'end')

    def _atualizar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        self.lista_clientes_cache = self.cliente_service.listar_clientes()
        
        for cli in self.lista_clientes_cache:
            end_str = f"{cli.endereco.rua}, {cli.endereco.numero} - {cli.endereco.bairro}"
            self.tree_clientes.insert('', 'end', values=(cli.id, cli.nome, cli.telefone, end_str))

    # =======================================================
    #                   ABA PEDIDOS (NOVO!)
    # =======================================================
    def _setup_aba_pedidos(self):
        # 1. Seleção de Cliente (Topo)
        frame_topo = tk.Frame(self.frame_pedidos)
        frame_topo.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_topo, text="Selecione o Cliente:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.combo_clientes = ttk.Combobox(frame_topo, width=50, state="readonly")
        self.combo_clientes.pack(side='left', padx=10)
        # Evento: Quando selecionar cliente, inicia um pedido
        self.combo_clientes.bind("<<ComboboxSelected>>", self._on_cliente_selecionado)

        # 2. Área Principal (Split: Cardápio | Ações | Carrinho)
        paned = ttk.PanedWindow(self.frame_pedidos, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=5)

        # --- Esquerda: Cardápio ---
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

        # --- Centro: Botões de Ação ---
        frame_acoes = tk.Frame(paned)
        paned.add(frame_acoes, weight=0) # weight 0 para não esticar muito

        ttk.Label(frame_acoes, text="Qtd:").pack(pady=(50, 5))
        self.entry_qtd = ttk.Entry(frame_acoes, width=5)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(pady=5)

        btn_add = ttk.Button(frame_acoes, text="Adicionar >>", command=self._adicionar_item)
        btn_add.pack(pady=20, padx=10)

        # --- Direita: Carrinho ---
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

        # 3. Rodapé (Total e Finalizar)
        frame_footer = tk.Frame(self.frame_pedidos, bg="#f0f0f0")
        frame_footer.pack(fill='x', padx=10, pady=10)

        self.lbl_total = ttk.Label(frame_footer, text="TOTAL: R$ 0.00", font=('Arial', 14, 'bold'), background="#f0f0f0")
        self.lbl_total.pack(side='right', padx=20)

        # Botão de finalizar deixaremos desativado até ter itens
        self.btn_finalizar = ttk.Button(frame_footer, text="Finalizar Pagamento", state="disabled")
        self.btn_finalizar.pack(side='right')

    # --- Lógica da Aba Pedidos ---

    def _atualizar_combo_clientes(self):
        """Popula o combobox com a lista de clientes (Cache em memória)"""
        # Reutiliza o cache da lista
        self.lista_clientes_cache = self.cliente_service.listar_clientes()
        
        valores_combo = []
        for c in self.lista_clientes_cache:
            valores_combo.append(f"{c.nome} ({c.telefone})")
        
        self.combo_clientes['values'] = valores_combo

    def _atualizar_cardapio(self):
        """Busca produtos do repo e põe no Treeview"""
        self.cardapio_cache = self.produto_repo.buscar_todos()
        
        for item in self.tree_cardapio.get_children():
            self.tree_cardapio.delete(item)
            
        for i, prod in enumerate(self.cardapio_cache):
            # Usamos o índice da lista (i) como ID no treeview (iid) para achar fácil depois
            tipo_nome = type(prod).__name__ # Pega 'Hamburguer', 'Bebida', etc
            self.tree_cardapio.insert('', 'end', iid=i, values=(prod.nome, f"R$ {prod.preco:.2f}", tipo_nome))

    def _on_cliente_selecionado(self, event):
        """Chamado quando usuário escolhe um cliente no Combo"""
        idx = self.combo_clientes.current()
        if idx >= 0:
            cliente = self.lista_clientes_cache[idx]
            self.cliente_selecionado_obj = cliente
            
            # Cria um NOVO pedido em memória para esse cliente
            self.pedido_atual = self.pedido_service.criar_pedido(cliente)
            
            # Limpa visualização do carrinho anterior
            self._atualizar_carrinho_view()
            print(f"Pedido iniciado para {cliente.nome}")

    def _adicionar_item(self):
        """Lógica do botão Adicionar >>"""
        # 1. Validações
        if not self.pedido_atual:
            messagebox.showwarning("Atenção", "Selecione um cliente primeiro para iniciar o pedido.")
            return

        selecionado = self.tree_cardapio.focus() # Pega o ID (iid) do item selecionado
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto no cardápio.")
            return
        
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade inválida.")
            return

        # 2. Recupera o objeto Produto real da lista cache
        idx_produto = int(selecionado)
        produto_obj = self.cardapio_cache[idx_produto]

        # 3. Adiciona ao Pedido (Lógica de Negócio)
        self.pedido_service.adicionar_item(self.pedido_atual, produto_obj, qtd)

        # 4. Atualiza a tela
        self._atualizar_carrinho_view()

    def _atualizar_carrinho_view(self):
        """Reconstroi a lista do carrinho baseada no objeto self.pedido_atual"""
        # Limpa lista visual
        for item in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(item)
        
        # Reseta se não tiver pedido
        if not self.pedido_atual:
            self.lbl_total.config(text="TOTAL: R$ 0.00")
            self.btn_finalizar.config(state="disabled")
            return

        # Preenche lista
        # Nota: Acessando _itens diretamente para leitura na View (Pragmatismo UI)
        for item_pedido in self.pedido_atual._itens:
            self.tree_carrinho.insert('', 'end', values=(
                item_pedido.produto.nome,
                item_pedido.quantidade,
                f"R$ {item_pedido.subtotal:.2f}"
            ))
        
        # Atualiza Total
        total = self.pedido_atual.total
        self.lbl_total.config(text=f"TOTAL: R$ {total:.2f}")

        # Habilita botão se tiver itens
        if total > 0:
            self.btn_finalizar.config(state="normal")
        else:
            self.btn_finalizar.config(state="disabled")

if __name__ == "__main__":
    from database import init_db
    init_db()
    app = MainWindow()
    app.mainloop()