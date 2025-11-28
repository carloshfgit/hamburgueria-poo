import tkinter as tk
from tkinter import ttk, messagebox

class AbaClientes(tk.Frame):
    def __init__(self, parent, service):
        """
        :param parent: O widget pai (no nosso caso, o Notebook)
        :param service: Instância de ClienteService para regras de negócio
        """
        super().__init__(parent)
        self.service = service
        
        # Constrói a Interface
        self._setup_ui()
        
        # Carrega dados iniciais
        self._atualizar_lista_clientes()

    def _setup_ui(self):
        # Formulário
        lbl_frame_form = ttk.LabelFrame(self, text="Cadastrar Novo Cliente")
        lbl_frame_form.pack(fill='x', padx=10, pady=5)

        # Linha 0: Nome
        ttk.Label(lbl_frame_form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = ttk.Entry(lbl_frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        # Linha 0: Telefone
        ttk.Label(lbl_frame_form, text="Telefone:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_telefone = ttk.Entry(lbl_frame_form, width=20)
        self.entry_telefone.grid(row=0, column=3, padx=5, pady=5)

        # Linha 1: Cidade
        ttk.Label(lbl_frame_form, text="Cidade:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_cidade = ttk.Entry(lbl_frame_form, width=30)
        self.entry_cidade.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Botão Salvar
        btn_salvar = ttk.Button(lbl_frame_form, text="Salvar Cliente", command=self._salvar_cliente)
        btn_salvar.grid(row=2, column=0, columnspan=4, pady=10)

        # Listagem
        lbl_frame_lista = ttk.LabelFrame(self, text="Clientes Cadastrados")
        lbl_frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

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
            
            if not nome or not tel or not cidade:
                messagebox.showwarning("Aviso", "Todos os campos (Nome, Telefone, Cidade) são obrigatórios!")
                return

            # Uso do service injetado
            self.service.cadastrar_cliente(nome, tel, cidade)
            
            messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado!")
            
            self._limpar_campos_cliente()
            self._atualizar_lista_clientes()
            
            # Nota: A atualização do combobox de pedidos será tratada via callback ou recarga na etapa de integração
            
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao salvar: {e}")

    def _limpar_campos_cliente(self):
        for entry in [self.entry_nome, self.entry_telefone, self.entry_cidade]:
            entry.delete(0, 'end')

    def _atualizar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Busca direta do service
        lista_clientes = self.service.listar_clientes()
        
        for cli in lista_clientes:
            self.tree_clientes.insert('', 'end', values=(cli.id, cli.nome, cli.telefone, cli.cidade))