from models.hamburguer import Hamburguer
from models.bebida import Bebida
from models.pedido import Pedido
from models.processador_pagamento import ProcessadorPagamento
from models.cliente import Cliente
from models.acompanhamento import Acompanhamento
from models.endereco import Endereco

def main():

    print("Bem vindo a nossa hamburgueria!")

    #criando produtos do cardapio
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
        desc="Porção generosade batatas",
        tamanho="G"
    )

    nuggets_g = Acompanhamento(
        nome="Nuggets",
        preco=16.00,
        desc="Porção generosa de nuggets",
        tamanho="G"
    )

    #criando clientes e endereços
    endereco_joao = Endereco(rua="Rua das Flores", numero=123, bairro="Centro", cidade="São Paulo")
    cliente_joao = Cliente(nome="João Silva", telefone="11987654321", endereco=endereco_joao)

    #criando pedidos
    pedido_joao = Pedido(cliente=cliente_joao)
    pedido_joao.adicionar_item(x_tudo, 1)
    pedido_joao.adicionar_item(coca_cola, 2)
    pedido_joao.adicionar_item(fritas_g, 1)

    #exibindo resumo do pedido
    print("\nResumo do Pedido:")
    print(pedido_joao)

    #pagamento
    processador = ProcessadorPagamento()
    processador.processar(pedido=pedido_joao, forma_pagamento="Cartão de Crédito")
    
    #status do pedido
    print(f"\nStatus final do pedido: {pedido_joao._status}")

    #garantindo funcionamento do codigo
    if __name__ == "__main__":
        main()