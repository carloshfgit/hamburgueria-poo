# Arquivo: app.py

# Importações dos seus modelos (conforme seu arquivo original)
from models.hamburguer import Hamburguer
from models.bebida import Bebida
from models.pedido import Pedido
from models.processador_pagamento import ProcessadorPagamento
from models.cliente import Cliente
from models.acompanhamento import Acompanhamento
from models.endereco import Endereco

# --- 1. Funções de "Setup" ---

def carregar_cardapio():
    """
    Cria e retorna a lista de produtos disponíveis (nosso cardápio).
    """
    print("Carregando cardápio...")
    
    # Produtos do cardápio 
    x_tudo = Hamburguer(
        nome="X-Tudo Monstro",
        preco=25.50,
        desc="O mais completo",
        ingredientes=["Pão", "Hambúrguer de 180g", "Queijo", "Bacon", "Ovo", "Alface", "Tomate"]
    )

    x_salada = Hamburguer(
        nome="Monstro Fit",
        preco=22.50,
        desc="Equilíbrio e sabor",
        ingredientes=["Pão", "Hambúrguer de 180g", "Queijo", "Alface", "Tomate"]
    )

    coca_cola = Bebida(
        nome="Coca-Cola",
        preco=8.00,
        desc="Lata",
        volume_ml=350
    )

    suco_maracuja = Bebida(
        nome="Suco de Maracujá",
        preco=8.00,
        desc="Copo de 350ml",
        volume_ml=350
    )

    fritas_g = Acompanhamento(
        nome="Batata Frita",
        preco=12.00,
        desc="Porção generosa de batatas",
        tamanho="G"
    )

    nuggets_g = Acompanhamento(
        nome="Nuggets",
        preco=16.00,
        desc="Porção generosa de nuggets",
        tamanho="G"
    )
    
    return [x_tudo, x_salada, coca_cola, suco_maracuja, fritas_g, nuggets_g]

# --- 2. Funções Auxiliares (Exibição) ---

def exibir_menu_principal():
    """
    Exibe as opções principais do sistema para o operador.
    """
    print("\n--- 🍔 Hamburgueria POO - Sistema do Caixa 🍔 ---")
    print("1. Criar Novo Pedido")
    print("2. Cadastrar Novo Cliente")
    print("3. Listar Pedidos (Histórico)")
    print("4. Listar Clientes Cadastrados")
    print("5. Cancelar Pedido")
    print("0. Sair do Sistema")

def exibir_cardapio(cardapio):
    """
    Exibe os itens do cardápio para seleção.
    """
    print("\n--- Cardápio Disponível ---")
    for i, produto in enumerate(cardapio):
        
        # <<< MUDANÇA: de _nome, _descricao e get_preco() para .nome, .descricao e .preco >>>
        print(f"{i + 1}. {produto.nome} ({produto.descricao}) - R${produto.preco:.2f}")
        
def pausar_e_limpar():
    """
    Pausa a execução e espera o usuário pressionar Enter.
    """
    input("\nPressione Enter para continuar...")
    # Em um terminal de verdade, você poderia adicionar:
    # import os
    # os.system('cls' if os.name == 'nt' else 'clear')

# --- 3. Funções de Funcionalidades ---


def cadastrar_cliente(lista_clientes):
    """
    Pede os dados, cria um novo Cliente e Endereco, e o adiciona à lista.
    """
    print("\n--- Cadastro de Novo Cliente ---")
    nome = input("Nome do cliente: ")
    telefone = input("Telefone (ex: 11987654321): ")
    
    print("\nEndereço do Cliente:")
    rua = input("Rua: ")
    numero = input("Número: ") 
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    
    try:
        
        novo_endereco = Endereco(rua=rua, numero=numero, bairro=bairro, cidade=cidade)
        novo_cliente = Cliente(nome=nome, telefone=telefone, endereco=novo_endereco)
        
        lista_clientes.append(novo_cliente)
        print(f"\n✅ Cliente '{nome}' cadastrado com sucesso!")
        return novo_cliente
    except Exception as e:
        print(f"\n❌ Erro ao cadastrar cliente: {e}")
        return None


def selecionar_cliente(lista_clientes):
    """
    Exibe os clientes cadastrados e permite ao operador selecionar um ou cadastrar um novo.
    Retorna o objeto Cliente selecionado.
    """
    if not lista_clientes:
        print("\nNenhum cliente cadastrado. Vamos cadastrar o primeiro.")
        return cadastrar_cliente(lista_clientes)

    print("\n--- Selecionar Cliente ---")
    for i, cliente in enumerate(lista_clientes):
        
        # <<< MUDANÇA: de _nome e _telefone para .nome e .telefone >>>
        print(f"{i + 1}. {cliente.nome} ({cliente.telefone})")
    
    print("-------------------------")
    print("N. Cadastrar NOVO cliente")
    
    while True:
        escolha = input("Digite o número do cliente ou 'N' para novo: ").strip().upper()
        
        if escolha == 'N':
            return cadastrar_cliente(lista_clientes)
        
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(lista_clientes):
                cliente_selecionado = lista_clientes[indice]
                
                # <<< MUDANÇA: de _nome para .nome >>>
                print(f"Cliente '{cliente_selecionado.nome}' selecionado.")
                return cliente_selecionado
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número ou 'N'.")

def criar_pedido(lista_pedidos, lista_clientes, cardapio):
    """
    Conduz o processo de criação de um novo pedido.
    """
    print("\n--- Criação de Novo Pedido ---")
    
    # 1. Selecionar o Cliente
    cliente_do_pedido = selecionar_cliente(lista_clientes)
    if not cliente_do_pedido:
        print("Criação de pedido cancelada (nenhum cliente selecionado).")
        return

    # Assumindo que Pedido(cliente=...) espera o objeto cliente
    novo_pedido = Pedido(cliente=cliente_do_pedido)
    
    # 2. Adicionar Itens
    print("\n--- Adicionar Itens ao Pedido ---")
    while True:
        exibir_cardapio(cardapio)
        print("------------------------------")
        print("Digite '0' para finalizar o pedido.")
        
        escolha_produto = input("Digite o número do produto: ")
        
        if escolha_produto == '0':
            # (Verificação de itens mínimos pode ser feita aqui ou no modelo)
            break 
            
        try:
            indice_produto = int(escolha_produto) - 1
            if not (0 <= indice_produto < len(cardapio)):
                print("Número de produto inválido.")
                continue
                
            produto_selecionado = cardapio[indice_produto]
            
            # Sub-loop para quantidade
            while True:
                try:
                    # --- CORREÇÃO AQUI ---
                    quantidade = int(input(f"Quantidade de '{produto_selecionado.nome}': "))
                    if quantidade > 0:
                        break
                    else:
                        print("Quantidade deve ser positiva.")
                except ValueError:
                    print("Digite um número válido.")
            
            # O print() foi removido de adicionar_item
            novo_pedido.adicionar_item(produto_selecionado, quantidade) 
            
            # --- CORREÇÃO AQUI ---
            # O app.py agora é responsável pela mensagem de feedback
            print(f"✅ {quantidade}x {produto_selecionado.nome} adicionado(s).")
            # <<< MUDANÇA: Correção de calcular_total() para .total >>>
            # Usando a @property 'total' definida em pedido.py
            print(f"Subtotal atual: R${novo_pedido.total:.2f}") 

        except ValueError:
            print("Entrada inválida. Digite o número do produto.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    # 3. Exibir Resumo e Processar Pagamento
    print("\n--- Resumo do Pedido ---")
    print(novo_pedido) # Usa o método __str__ da sua classe Pedido
    
    forma_pagamento = input("Forma de pagamento (Cartão de Crédito, PIX, Dinheiro): ")
    
    processador = ProcessadorPagamento()
    processador.processar(pedido=novo_pedido, forma_pagamento=forma_pagamento)
    
    # 4. Salvar e confirmar
    lista_pedidos.append(novo_pedido)
    print("\n✅ Pedido finalizado e pago com sucesso!")
    # <<< MUDANÇA: Usando a propriedade .status >>>
    print(f"Status final do pedido: {novo_pedido.status}") # Antes era _status

def listar_pedidos(lista_pedidos):
    """
    Exibe um histórico de todos os pedidos realizados.
    """
    print("\n--- Histórico de Pedidos ---")
    if not lista_pedidos:
        print("Nenhum pedido registrado no sistema.")
        return
        
    for i, pedido in enumerate(lista_pedidos):
        print(f"\n--- Pedido {i + 1} ---")
        print(pedido) # Confia no __str__ do Pedido
        # <<< MUDANÇA: Usando a propriedade .status >>>
        print(f"Status: {pedido.status}") # Antes era _status
        print("-" * 20)

def listar_clientes(lista_clientes):
    """
    Exibe todos os clientes cadastrados.
    """
    print("\n--- Clientes Cadastrados ---")
    if not lista_clientes:
        print("Nenhum cliente cadastrado no sistema.")
        return
        
    for i, cliente in enumerate(lista_clientes):
        
        # Esta linha já está correta (graças ao refatoramento anterior)
        endereco = cliente.endereco
        
        # <<< MUDANÇA: de _rua, _numero, etc. para .rua, .numero, etc. >>>
        # Agora o encapsulamento de Endereco está sendo respeitado!
        end_str = f"{endereco.rua}, {endereco.numero} - {endereco.bairro}, {endereco.cidade}"
        
        print(f"\n--- Cliente {i + 1} ---")
        # Estas linhas já estão corretas (graças ao refatoramento anterior)
        print(f"Nome: {cliente.nome}")
        print(f"Telefone: {cliente.telefone}")
        print(f"Endereço: {end_str}")
        print("-" * 20)


def cancelar_pedido(lista_pedidos):
    """
    Permite ao operador selecionar um pedido e alterar seu status para 'Cancelado'.
    A lógica de cancelamento foi movida para a classe Pedido.
    """
    print("\n--- Cancelar Pedido ---")
    if not lista_pedidos:
        print("Nenhum pedido registrado para cancelar.")
        return
    
    # Lista pedidos para escolha
    for i, pedido in enumerate(lista_pedidos):
        # <<< MUDANÇA: de pedido.cliente._nome para pedido.cliente.nome >>>
        print(f"{i + 1}. Pedido de {pedido.cliente.nome} (Status: {pedido.status}) - Total: R${pedido.total:.2f}")

    
    try:
        escolha = int(input("\nDigite o número do pedido que deseja cancelar: "))
        indice = escolha - 1
        
        if not (0 <= indice < len(lista_pedidos)):
            print("Número de pedido inválido.")
            return
            
        pedido_a_cancelar = lista_pedidos[indice]
        
        # <<< MUDANÇA: Delegação da lógica para o modelo >>>

        resultado = pedido_a_cancelar.cancelar()
        
        # O app.py (Visão) agora só exibe a mensagem com base no resultado
        if resultado == "sucesso":
            print("✅ Pedido cancelado com sucesso.")
        elif resultado == "ja_cancelado":
            print("Este pedido já está cancelado.")
        elif resultado == "cancelado_pago":
            print(f"Atenção: Este pedido já foi pago.")
            print("✅ Pedido cancelado (estorno manual necessário).")
            
    except ValueError:
        print("Entrada inválida. Digite um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# --- 4. Função Principal (Loop do Aplicativo) ---

def iniciar_sistema(): 
    """
    Função principal que roda o loop do aplicativo de caixa.
    """
    # Dados em memória do sistema
    cardapio = carregar_cardapio()
    clientes = []
    pedidos = []
    
    print("\nBem-vindo à Hamburgueria POO!")

    while True:
        exibir_menu_principal()
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            criar_pedido(pedidos, clientes, cardapio)
            pausar_e_limpar()
        
        elif opcao == '2':
            cadastrar_cliente(clientes)
            pausar_e_limpar()
            
        elif opcao == '3':
            listar_pedidos(pedidos)
            pausar_e_limpar()
            
        elif opcao == '4':
            listar_clientes(clientes)
            pausar_e_limpar()
            
        elif opcao == '5':
            cancelar_pedido(pedidos)
            pausar_e_limpar()
            
        elif opcao == '0':
            print("\nObrigado por usar o sistema. Saindo...")
            break
            
        else:
            print("\nOpção inválida. Por favor, tente novamente.")
            pausar_e_limpar()