#  Hamburgueria POO - Sistema de Gestão

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?style=for-the-badge&logo=sqlite)
![Tkinter](https://img.shields.io/badge/Interface-Tkinter-orange?style=for-the-badge)

Um sistema completo de gerenciamento de pedidos para uma hamburgueria, desenvolvido em **Python**. O projeto foi concebido com foco em boas práticas de Engenharia de Software, utilizando **Arquitetura em Camadas** e conceitos avançados de **Programação Orientada a Objetos (POO)**.

---

##  Sobre o Projeto

Este projeto simula o fluxo real de um sistema de caixa (PDV), permitindo o cadastro de clientes, a montagem de pedidos complexos (com hambúrgueres, bebidas e acompanhamentos), processamento de pagamentos e histórico de vendas.

O diferencial técnico é a sua estrutura robusta, desacoplando a interface gráfica das regras de negócio e do acesso ao banco de dados.

###  Funcionalidades Principais

###  Funcionalidades Principais

* **Interface Gráfica Moderna:** Navegação por abas (Clientes, Pedidos, Histórico) desenvolvida com `Tkinter`.
* **Gestão de Clientes:** Cadastro completo com validação de dados.
* **Cardápio Polimórfico:** Suporte a diferentes tipos de produtos (`Hamburguer`, `Bebida`, `Acompanhamento`) tratados de forma genérica pelo sistema.
* **Carrinho de Compras:** Adição dinâmica de itens, cálculo de subtotal e total em tempo real.
* **Gestão de Histórico:** Visualização detalhada dos itens de cada pedido e funcionalidade de **cancelamento de pedidos** com estorno de status.
* **Pagamentos:** Simulação de pagamentos (Dinheiro, Cartão, Pix).
* **Persistência de Dados:** Banco de dados SQLite (`hamburgueria.db`) gerado e gerenciado automaticamente.
* **Modo Híbrido:** Possui tanto uma interface gráfica quanto uma versão em linha de comando (Console/CLI).

---

##  Como Executar

### Pré-requisitos
* Python 3.8 ou superior instalado.
* Bibliotecas padrão do Python (o projeto não exige `pip install` de pacotes externos complexos, pois usa `sqlite3` e `tkinter` nativos).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/hamburgueria-poo.git](https://github.com/seu-usuario/hamburgueria-poo.git)
    cd hamburgueria-poo
    ```

2.  **Execute a Interface Gráfica (Recomendado):**
    ```bash
    python run_gui.py
    ```

3.  **Execute a Versão Console (Legado):**
    ```bash
    python main.py
    ```

> **Nota:** Na primeira execução, o sistema criará automaticamente o arquivo `hamburgueria.db` e populará o cardápio inicial.

---

##  Arquitetura e Tecnologias

O projeto segue estritamente a **Layered Architecture** (Arquitetura em Camadas), facilitando a manutenção e a escalabilidade.

### Estrutura de Diretórios
```text
hamburgueria-poo/
│
├── models/              # Entidades do Domínio (Regras de Estado)
│   ├── cliente.py       # Ex: Cliente
│   ├── pedido.py        # Lógica de totais e itens
│   ├── produto.py       # Classe Abstrata (Herança)
│   └── ...
│
├── repositories/        # Camada de Acesso a Dados (SQL/Persistence)
│   ├── cliente_repository.py
│   └── pedido_repository.py
│
├── services/               # Regras de Negócio (Lógica Pura)
│   ├── cliente_service.py  # Ex: Validação de duplicidade
│   └── pedido_service.py   # Orquestração do pedido
│
├── views/               # Camada de Apresentação
│   ├── console_view.py     # Interface CLI
│   └── graficos/           # Interface Gráfica (Tkinter)
│       ├── main_window.py  # Orquestrador da Janela
│       └── abas/           # Módulos da Interface
│           ├── aba_clientes.py
│           ├── aba_historico.py
│           └── aba_pedidos.py
│
├── controllers/         # Orquestradores (Legacy/Console)
├── database.py          # Configuração do SQLite
└── run_gui.py           # Entry Point da Interface Gráfica