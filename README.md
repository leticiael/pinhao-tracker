# Pinhão Tracker

Sistema de gestão da produção de pinhão (semente da *Araucaria angustifolia*) para pequenos produtores da região de **Campina Grande do Sul** e **Quatro Barras**, no Paraná. Projeto acadêmico FIAP 2026.

## O problema do agronegócio

Pequenos produtores extrativistas de pinhão do Primeiro Planalto Paranaense operam, em sua maioria, sem nenhum tipo de controle sistemático da produção. Toda a gestão é feita em cadernos, papéis avulsos ou na memória, o que gera quatro consequências diretas e recorrentes:

1. **Desconhecimento da produtividade real por safra.** Sem registrar kg colhidos por dia e por propriedade, o produtor não consegue avaliar se sua produção melhorou, estagnou ou caiu ao longo dos anos.
2. **Ausência de histórico climático.** A produção da araucária é altamente sensível a temperatura, umidade e regime de chuvas. Sem um histórico climático atrelado aos registros de colheita, é impossível correlacionar variações anuais de produtividade a condições meteorológicas.
3. **Venda no momento errado.** O preço do pinhão oscila fortemente dentro da própria safra (15 de abril a 30 de junho, conforme a Instrução Normativa IAT nº 03/2026). Sem histórico de preços, o produtor vende no primeiro comprador que aparece — geralmente atravessadores — perdendo margem.
4. **Perdas pós-colheita.** Pinhão é altamente perecível. Armazenado a granel, dura cerca de 30 dias; a vácuo refrigerado, até 120 dias; e congelado, até 210 dias. Sem controle do método e da data de entrada em estoque, produtos vencem dentro do armazém e viram prejuízo.

O **Pinhão Tracker** resolve essas quatro dores com cadastros estruturados, alertas automáticos e relatórios comparativos entre safras.

## Por que Campina Grande do Sul e Quatro Barras

Os dois municípios estão no coração da **Rota do Pinhão**, circuito turístico e gastronômico criado pelo governo do Paraná que reúne os pontos de maior concentração de araucárias nativas do estado. A região reúne três características que a tornam estratégica:

- **Altitude acima de 800 metros** na Serra do Mar paranaense, condição ideal para a *Araucaria angustifolia*.
- **Temperatura média anual entre 15 °C e 25 °C**, dentro da faixa ótima para a espécie.
- **Cooperativismo ativo**, com destaque para a **Cooperativa Nascente**, que agrega pequenos produtores extrativistas e reforça o papel do pinhão como fonte complementar de renda em propriedades familiares.

O extrativismo do pinhão é, nessas duas cidades, uma renda sazonal relevante em propriedades que combinam agricultura familiar, turismo rural e produção de erva-mate. Uma ferramenta simples de gestão aumenta o poder de barganha do produtor e ajuda a preservar a araucária, espécie criticamente ameaçada de extinção.

## Solução proposta

O Pinhão Tracker é um sistema de terminal, escrito em Python 3.12+, que oferece:

- **Cadastro de propriedade e árvores** (quantidade, tipo nativa ou enxertada, idade estimada), com alertas sobre altitude e idade produtiva.
- **Registro de colheita diária** (data, kg coletados, método chão ou escalada, uso de EPI), com validação do período oficial de safra e cálculo de multa estimada para coletas fora do período.
- **Monitoramento climático** com registro manual ou importação em lote via arquivo `.txt`, com avaliação de temperatura e umidade contra as faixas ideais.
- **Controle de armazenamento pós-colheita** com cálculo automático de vencimento conforme o método (granel, vácuo refrigerado, congelado) e alertas visuais de validade.
- **Registro de preços e análise de momento de venda**, comparando preço atual com média histórica, preço mínimo federal PGPM-Bio e referências regionais para sugerir **vender agora** ou **aguardar**.
- **Relatórios**: produtividade por safra, comparativo entre anos (variação absoluta e percentual) e custo versus receita com cálculo de margem líquida.
- **Log de operações** em `.txt` e **exportação de dados** em `.json`.

### Dados científicos embutidos

| Parâmetro | Valor |
|---|---|
| Período oficial de safra no PR | 15/04 a 30/06 (IAT nº 03/2026) |
| Pinhões por pinha | 100 a 120 |
| Idade produtiva — araucária nativa | 12 a 15 anos |
| Idade produtiva — araucária enxertada | 6 a 8 anos |
| Temperatura média anual ideal | 15 °C a 25 °C |
| Altitude ideal | acima de 800 m |
| Armazenamento a granel | ~30 dias |
| Armazenamento a vácuo refrigerado | ~120 dias |
| Armazenamento congelado | até 210 dias |
| Preço mínimo federal PGPM-Bio 2024 | R$ 3,66/kg |
| Preço médio ao produtor 2025 (Serra Catarinense) | R$ 6,44/kg |
| Multa por coleta fora da safra | R$ 300 a cada 50 kg apreendidos |

## Requisitos técnicos atendidos

- **Subalgoritmos**: todas as funcionalidades estão organizadas em funções com passagem de parâmetros.
- **Estruturas de dados**: uso de **listas** (coleções de registros), **tuplas** (opções imutáveis de menu, faixas etárias) e **dicionários** (configuração, registros individuais, agregações).
- **Manipulação de arquivos**: `.txt` para log de operações e importação de clima; `.json` para configuração e exportação.
- **Banco de dados Oracle** via biblioteca `oracledb`, com **fallback gracioso para JSON** caso o servidor não esteja disponível ou as tabelas não estejam criadas.

## Instalação

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install oracledb
```

> Python 3.12 ou superior é necessário. A única dependência externa é `oracledb`. O sistema funciona sem `oracledb` instalado: opera em modo JSON automaticamente.

## Configuração do Oracle (opcional)

1. Tenha um Oracle Database acessível (local ou remoto).
2. Ajuste as credenciais em `config.json` no bloco `"oracle"` (`user`, `password`, `dsn`).
3. Execute o script DDL para criar as tabelas:

```bash
sqlplus seu_usuario/sua_senha@seu_dsn @setup_database.sql
```

Sem Oracle configurado, o sistema usa `dados/dados.json` como armazenamento.

## Execução

```bash
python main.py
```

O menu principal será exibido. Todas as operações são acessadas por submenus numerados.

### Importação de clima a partir de `.txt`

O arquivo `dados/clima_exemplo.txt` ilustra o formato esperado:

```
DD/MM/AAAA;temperatura;umidade;precipitacao
15/04/2026;14.2;85.0;8.5
```

Linhas iniciadas por `#` são tratadas como comentário e ignoradas.

## Estrutura do projeto

```
pinhao-tracker/
├── main.py                      # Ponto de entrada
├── config.json                  # Configurações e dados científicos
├── setup_database.sql           # DDL das tabelas Oracle
├── README.md
├── dados/
│   ├── clima_exemplo.txt        # Arquivo exemplo para importação
│   ├── dados.json               # Gerado em tempo de execução (modo JSON)
│   ├── exportacao.json          # Gerado na exportação
│   └── log_operacoes.txt        # Gerado em tempo de execução
└── modules/
    ├── __init__.py
    ├── arquivo.py               # I/O de .txt e .json
    ├── armazenamento.py         # Controle pós-colheita
    ├── clima.py                 # Monitoramento climático
    ├── colheita.py              # Registro diário de colheita
    ├── database.py              # Oracle + fallback JSON
    ├── menu.py                  # Menus e navegação
    ├── precos.py                # Preços e recomendação de venda
    ├── propriedade.py           # Propriedades e árvores
    ├── relatorios.py            # Relatórios consolidados
    └── validacao.py             # Validação de entradas
```

## Dependências

- Python 3.12+
- `oracledb` (opcional — sistema tem fallback para JSON)

## Repositório

GitHub: [leticiael/pinhao-tracker](https://github.com/leticiael/pinhao-tracker)
