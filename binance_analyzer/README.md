# Binance Analyzer

Um projeto Python para análise de dados da Binance, incluindo preços históricos, saldos de conta e geração de gráficos.

## Estrutura do Projeto

```
binance_analyzer/
├── src/
│   ├── __init__.py
│   ├── database_manager.py
│   ├── binance_api.py
│   └── binance_analyzer.py
├── main.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.6+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

Certifique-se de que o arquivo `.config` está configurado corretamente com suas credenciais da Binance e do banco de dados Oracle.

## Uso

Carregue as variáveis de ambiente:
```bash
. .config.env
```

Execute o programa principal:
```bash
python main.py
```

## Funcionalidades

- Consulta de saldo da conta Binance
- Análise de preços históricos
- Geração de gráficos de preços
- Integração com banco de dados Oracle 