# Automação para certificado II Robocorp - RPA

Automação desenvolvida com **Robocorp** para realizar pedidos de robôs no site RobotSpareBin Industries Inc.

## Sobre o projeto

O robô automatiza o processo de pedidos no RobotSpareBin, utilizando os dados fornecidos no arquivo `orders.csv`.

Para cada pedido, o robô:

- Acessa o site RobotSpareBin
- Baixa automaticamente o arquivo de pedidos
- Preenche o formulário de pedido
- Seleciona as partes do robô
- Preenche o endereço de entrega
- Realiza o pedido
- Captura uma imagem do robô
- Gera um recibo em PDF
- Armazena os resultados na pasta `robots`

## Tecnologias utilizadas

- Python
- Robocorp
- Robocorp Browser
- RPA Framework
- Playwright
- Robocorp Tasks

## Estrutura do projeto

```text
.
├── conda.yaml
├── robot.yaml
├── tasks.py
├── README.md
└── robots/
    ├── pdfs/
    └── robots_pngs/
