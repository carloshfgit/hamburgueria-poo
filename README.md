# Hamburgueria POO - Sistema de Gestão de Pedidos


## Sobre o Projeto

Este projeto é uma simulação de um sistema de gerenciamento para uma hamburgueria, desenvolvido com o objetivo principal de aplicar conceitos avançados de **Programação Orientada a Objetos (POO)** e **Arquitetura de Software**.

O sistema permite o cadastro de clientes, criação de pedidos complexos (hambúrgueres, bebidas, acompanhamentos), simulação de pagamentos e persistência de dados, tudo estruturado para seguir boas práticas de engenharia de software (SOLID).

---

## Arquitetura e Tecnologias

O projeto evoluiu de um script procedural para uma **Arquitetura em Camadas (Layered Architecture)**, visando desacoplamento e escalabilidade.

### Estrutura de Camadas
* **Models:** Classes de domínio que representam as entidades do negócio (Cliente, Pedido, Produto) com seus comportamentos e regras de estado.
* **Repositories:** Responsáveis exclusivamente pela persistência de dados e comunicação SQL com o banco de dados (SQLite).
* **Services:** Camada de regras de negócio. Orquestra as validações, cálculos e chama os repositórios.
* **Controllers:** Gerenciam o fluxo da aplicação, recebendo inputs da View e delegando para os Services.
* **Views:** Responsável pela interação com o usuário. Atualmente via Console (CLI), mas preparada para migração futura para Interface Gráfica (Tkinter).

### Conceitos de POO Aplicados
* **Abstração:** Uso de classes base (como `Produto`) para definir contratos.
* **Herança:** Especialização de classes (`Hamburguer`, `Bebida` herdam de `Produto`).
* **Encapsulamento:** Proteção de atributos e uso de Properties.
* **Polimorfismo:** Tratamento genérico de itens no pedido, independente do tipo específico.

---

## Funcionalidades

-  **Cadastro de Clientes:** Registro com validação de unicidade (telefone) e endereço vinculado.
-  **Gestão de Pedidos:**
    - Adição de múltiplos itens.
    - Cálculo automático de subtotal e total.
    - Histórico de pedidos por cliente.
-  **Persistência de Dados:** Todos os registros são salvos automaticamente em banco de dados SQLite (`hamburgueria.db`).
-  **Controle de Status:** Fluxo de estados do pedido (Recebido -> Pago -> Cancelado).
-  **Histórico de Preços:** O sistema grava o preço do item no momento da venda, garantindo integridade histórica mesmo se o cardápio mudar.

---

## Estrutura de Arquivos

```text
hamburgueria_poo/
│
├── controllers/         # Controladores de fluxo (MainController)
├── models/              # Entidades (Cliente, Pedido, Produto, etc.)
├── repositories/        # Acesso a Dados (SQL Operations)
├── services/            # Regras de Negócio (ClienteService, PedidoService)
├── views/               # Interfaces (ConsoleView)
│
├── database.py          # Configuração e conexão com SQLite
├── main.py              # Ponto de entrada da aplicação
├── hamburgueria.db      # Arquivo do Banco de Dados (gerado automaticamente)
└── UML-hamburgueriaa-poo.png # Diagrama de Classes