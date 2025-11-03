import database
from models.hamburguer import Hamburguer
from models.bebida import Bebida
from models.pedido import Pedido
from models.processador_pagamento import ProcessadorPagamento
from models.cliente import Cliente
from models.acompanhamento import Acompanhamento
from models.endereco import Endereco

#funções de inicialização

#cria e retorna a lista do cardapio
def carregar_cardapio():
    
    print("Carregando cardápio...")
    
    #criando nosso cardápio 
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

#funções de exibição do menu

def exibir_menu_principal():

    print("\n--- 🍔 Hamburgueria POO - Sistema do Caixa 🍔 ---")
    print("1. Criar Novo Pedido")
    print("2. Cadastrar Novo Cliente")
    print("3. Listar Pedidos (Histórico)")
    print("4. Listar Clientes Cadastrados")
    print("5. Cancelar Pedido")
    print("0. Sair do Sistema")

#exibe-se os itens do cardapio para selecionar
def exibir_cardapio(cardapio):

    print("\n--- Cardápio Disponível ---")
    for i, produto in enumerate(cardapio):
        print(f"{i + 1}. {produto.nome} ({produto.descricao}) - R${produto.preco:.2f}")

#pausa a execução e espera o input do enter      
def pausar_e_limpar():
    input("\nPressione Enter para continuar...")

#funções de operações

#pede os dados, cria um novo Cliente e Endereco, e o adiciona à lista.
def cadastrar_cliente(lista_clientes):
    
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
        
        # --- Alteração aqui ---
        # Salva no banco de dados E atualiza o objeto com o ID
        novo_cliente = database.salvar_cliente(novo_cliente)
        
        lista_clientes.append(novo_cliente)
        print(f"\n✅ Cliente '{nome}' cadastrado com sucesso (ID: {novo_cliente.id})!")
        return novo_cliente
    except Exception as e:
        # Se o telefone for duplicado, o DB (UNIQUE) vai gerar um erro
        if "UNIQUE constraint failed" in str(e):
            print(f"\n❌ Erro: Telefone '{telefone}' já cadastrado.")
        else:
            print(f"\n❌ Erro ao cadastrar cliente: {e}")
        return None

#exibe os clientes cadastrados e permite ao operador selecionar um ou cadastrar um novo.
def selecionar_cliente(lista_clientes):
    
    if not lista_clientes:
        print("\nNenhum cliente cadastrado. Vamos cadastrar o primeiro.")
        return cadastrar_cliente(lista_clientes)

    print("\n--- Selecionar Cliente ---")
    for i, cliente in enumerate(lista_clientes):
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
                print(f"Cliente '{cliente_selecionado.nome}' selecionado.")
                return cliente_selecionado
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número ou 'N'.")

#criação do pedido
def criar_pedido(lista_pedidos, lista_clientes, cardapio):

    print("\n--- Criação de Novo Pedido ---")
    
    #seleciona o cliente desejado
    cliente_do_pedido = selecionar_cliente(lista_clientes)
    if not cliente_do_pedido:
        print("Criação de pedido cancelada (nenhum cliente selecionado).")
        return

    novo_pedido = Pedido(cliente=cliente_do_pedido)
    
    #adiciona os itens
    print("\n--- Adicionar Itens ao Pedido ---")
    while True:
        exibir_cardapio(cardapio)
        print("------------------------------")
        print("Digite '0' para finalizar o pedido.")
        
        escolha_produto = input("Digite o número do produto: ")
        
        if escolha_produto == '0':
            #verifica itens mínimos
            break 
            
        try:
            indice_produto = int(escolha_produto) - 1
            if not (0 <= indice_produto < len(cardapio)):
                print("Número de produto inválido.")
                continue
                
            produto_selecionado = cardapio[indice_produto]
            
            #loop para verificar quantidade valida
            while True:
                try:
                    quantidade = int(input(f"Quantidade de '{produto_selecionado.nome}': "))
                    if quantidade > 0:
                        break
                    else:
                        print("Quantidade deve ser positiva.")
                except ValueError:
                    print("Digite um número válido.")
            
            novo_pedido.adicionar_item(produto_selecionado, quantidade) 
            
            #confirma os produtos adicionados e printa o total
            print(f"✅ {quantidade}x {produto_selecionado.nome} adicionado(s).")
            print(f"Subtotal atual: R${novo_pedido.total:.2f}") 

        except ValueError:
            print("Entrada inválida. Digite o número do produto.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    #exibe o resumo do pedido e simula o pagamento
    print("\n--- Resumo do Pedido ---")
    print(novo_pedido) #usando metodo _str_ da classe pedido
    
    forma_pagamento = input("Forma de pagamento (Cartão de Crédito, PIX, Dinheiro): ")
    
    processador = ProcessadorPagamento()
    processador.processar(pedido=novo_pedido, forma_pagamento=forma_pagamento)
    
    # --- Alteração aqui ---
    # Salva o pedido no banco de dados DEPOIS que ele foi pago
    novo_pedido = database.salvar_pedido(novo_pedido)
    # Salva na lista em memória
    lista_pedidos.append(novo_pedido)
    print("\n✅ Pedido finalizado, pago e salvo no banco de dados!")
    print(f"Status final do pedido: {novo_pedido.status}")

#exibe o histórico de pedidos
def listar_pedidos(lista_pedidos):

    print("\n--- Histórico de Pedidos ---")
    if not lista_pedidos:
        print("Nenhum pedido registrado no sistema.")
        return
        
    for i, pedido in enumerate(lista_pedidos):
        print(f"\n--- Pedido {i + 1} ---")
        print(pedido)
        print(f"Status: {pedido.status}")
        print("-" * 20)

#exibe clientes cadastrados
def listar_clientes(lista_clientes):

    print("\n--- Clientes Cadastrados ---")
    if not lista_clientes:
        print("Nenhum cliente cadastrado no sistema.")
        return
        
    for i, cliente in enumerate(lista_clientes):
        
        endereco = cliente.endereco
        end_str = f"{endereco.rua}, {endereco.numero} - {endereco.bairro}, {endereco.cidade}"
        
        print(f"\n--- Cliente {i + 1} ---")
        print(f"Nome: {cliente.nome}")
        print(f"Telefone: {cliente.telefone}")
        print(f"Endereço: {end_str}")
        print("-" * 20)

#seleciona e cancela um pedido
def cancelar_pedido(lista_pedidos):

    print("\n--- Cancelar Pedido ---")
    if not lista_pedidos:
        print("Nenhum pedido registrado para cancelar.")
        return
    
    # exibe a lista pedidos para escolha
    for i, pedido in enumerate(lista_pedidos):
        
        print(f"{i + 1}. Pedido de {pedido.cliente.nome} (Status: {pedido.status}) - Total: R${pedido.total:.2f}")

    
    try:
        escolha = int(input("\nDigite o número do pedido que deseja cancelar: "))
        indice = escolha - 1
        
        if not (0 <= indice < len(lista_pedidos)):
            print("Número de pedido inválido.")
            return
            
        pedido_a_cancelar = lista_pedidos[indice]
        resultado = pedido_a_cancelar.cancelar()
        
        # --- Alteração aqui ---
        # Se o cancelamento foi bem-sucedido, atualiza no DB
        if resultado == "sucesso" or resultado == "cancelado_pago":
            database.atualizar_status_pedido(pedido_a_cancelar)
            print("✅ Pedido cancelado com sucesso (status atualizado no DB).")
        elif resultado == "ja_cancelado":
            print("Este pedido já está cancelado.")
        elif resultado == "cancelado_pago":
            print(f"Atenção: Este pedido já foi pago.")
            print("✅ Pedido cancelado (estorno manual necessário).")
            
    except ValueError:
        print("Entrada inválida. Digite um número.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

#função principal que garante o loop do aplicativo
def iniciar_sistema(): 
    
    # --- Alterações aqui ---
    # 1. Inicializa o DB (cria tabelas se não existirem)
    database.init_db()
    
    # 2. Carrega dados do DB em vez de listas vazias
    cardapio = carregar_cardapio()
    clientes = database.carregar_clientes()
    pedidos = database.carregar_pedidos(clientes)
    
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