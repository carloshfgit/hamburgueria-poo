# Hamburgueria POO - Simulação em Python

## Descrição do Projeto

Este é um projeto acadêmico desenvolvido para aplicar e demonstrar os conceitos fundamentais da Programação Orientada a Objetos (POO) em Python. O sistema simula a gestão de pedidos de uma hamburgueria, desde a criação dos produtos até o processamento do pagamento.

## Funcionalidades e Conceitos Aplicados

O projeto foi estruturado para exemplificar os 4 pilares da POO e outras relações importantes entre classes:

* **Abstração:** A classe `Produto` é abstrata, definindo um modelo comum que não pode ser instanciado diretamente.
* **Herança:** As classes `Hamburguer`, `Bebida` e `Acompanhamento` herdam características da classe `Produto`.
* **Encapsulamento:** Os atributos das classes são protegidos (convenção `_` e `__`), e o acesso é feito por meio de métodos públicos, garantindo a integridade dos dados.
* **Polimorfismo:** A classe `Pedido` trabalha com uma lista de `Produto`, tratando objetos de diferentes classes (`Hamburguer`, `Bebida`, etc.) de maneira uniforme, por exemplo, ao calcular o total do pedido.
* **Composição:** Relações fortes onde um objeto "possui" outro (ex: `Pedido` é composto por `ItemPedido`).
* **Associação:** Relações mais fracas entre objetos (ex: `Cliente` faz um `Pedido`).

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Banco de Dados:** SQLite

## Como Executar o Projeto

1.  **Clone o repositório (se estiver no Git) ou baixe os arquivos.**

2.  **Navegue até a pasta raiz do projeto:**
    ```bash
    cd hamburgueria_poo
    ```

3.  **Execute o arquivo principal para iniciar a simulação:**
    ```bash
    python3 main.py
    ```

4.  **A saída da simulação será exibida no terminal.**

## Estrutura de Arquivos

O projeto está organizado com a seguinte estrutura de diretórios para separar as responsabilidades:

```bash
hamburgueria_poo/
│
├── models/
│   ├── __init__.py
│   ├── produto.py
│   ├── hamburguer.py
│   ├── bebida.py
│   ├── acompanhamento.py
│   ├── endereco.py
│   ├── cliente.py
│   ├── item_pedido.py
│   ├── pedido.py
│   └── processador_pagamento.py
│
├── app.py
├── database.py
├── hamburgueria.db
├── main.py
└── README.md