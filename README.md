# Pinhão Tracker

Sistema de gestão da produção de pinhão (semente da *Araucaria angustifolia*) para pequenos produtores da região de **Campina Grande do Sul** e **Quatro Barras**, no Paraná. Projeto acadêmico FIAP 2026.

## Por que esse projeto existe

Sou de Quatro Barras, no Primeiro Planalto Paranaense — uma das regiões com maior concentração remanescente de *Araucaria angustifolia* do estado. O pinhão é **tradição local**: integra a culinária, a economia sazonal e o calendário rural de Quatro Barras, Campina Grande do Sul e das demais cidades da Rota do Pinhão. Essa tradição explica o recorte do projeto — em vez de um sistema genérico de gestão agrícola, um sistema específico para pinhão, para esta microrregião, com os parâmetros reais da legislação vigente.

Nas propriedades familiares da região, a gestão da produção é quase sempre feita em **caderno de papel ou na memória**. O caderno tem limitações concretas que atrapalham o produtor na prática:

- **Consulta lenta** — recuperar um dado pontual exige folhear várias páginas ou abrir mais de um caderno.
- **Risco físico** — papel molha, rasga, queima, ou simplesmente é descartado ao longo dos anos.
- **Sem comparação automática** — confrontar a safra deste ano com a do ano passado exige refazer todas as contas à mão.
- **Sem alertas de vencimento** — se o produtor esquecer a data em que guardou um lote, só descobre o vencimento quando abre a embalagem e encontra produto estragado.
- **Sem referência de preço** — não há como comparar o valor oferecido pelo atravessador com a média histórica da própria propriedade.

Um **sistema específico** para a cadeia do pinhão, ao contrário do caderno, busca e filtra registros em segundos, calcula vencimentos automaticamente, compara anos e avisa em tempo útil. É exatamente o que o **Pinhão Tracker** faz, atuando sobre quatro frentes:

- **Registra colheita diária** com validação automática do período legal de safra (IAT nº 03/2026) e cálculo da multa estimada caso a coleta caia fora da janela permitida.
- **Controla armazenamento pós-colheita** com cálculo de validade por método (granel, vácuo refrigerado, congelado) e totalização das perdas em kg e em percentual, fechando o ciclo de controle de estoque.
- **Analisa o momento de venda** comparando o preço atual com a média histórica registrada e com o preço mínimo federal PGPM-Bio, gerando recomendação objetiva de vender ou aguardar.
- **Gera relatórios comparativos** de produtividade por safra e por propriedade, formando o histórico documental que serve de base para negociação com cooperativa e para solicitação de crédito rural.

## O pinhão em números

A narrativa acima é pessoal, mas o peso dela está nos dados públicos. Os principais:

- **Árvore criticamente ameaçada.** A *Araucaria angustifolia* é classificada como **criticamente ameaçada de extinção** pela IUCN (União Internacional para a Conservação da Natureza). Da Floresta com Araucárias original — estimada em cerca de **20 milhões de hectares** — restam hoje **menos de 3%** no Brasil. No Paraná, a situação é ainda mais dramática: sobra **menos de 0,4%** dos 8 milhões de hectares nativos originais. Cada árvore que ainda frutifica é uma sobrevivente estatística.

- **Paraná é o maior produtor nacional em valor.** Segundo a **Pesquisa de Produção da Extração Vegetal e da Silvicultura (PEVS/IBGE) de 2023**, o Paraná respondeu por **43,3% do valor de produção de pinhão do Brasil** — R$ 26,8 milhões dos R$ 61,9 milhões nacionais. Em volume, o estado disputa o primeiro lugar ano a ano com Minas Gerais: foi **38,5% do volume nacional em 2021** e 32,9% em 2023 (contra 33,8% de MG).

- **Tudo é extrativismo, nada é silvicultura.** O IBGE classifica a produção oficial de pinhão como **extração vegetal**, não silvicultura. Isso quer dizer que o volume sai de **árvores nativas em pé**, não de plantio comercial. Por isso a cadeia está estruturalmente nas mãos de famílias que vivem próximo a remanescentes de Floresta com Araucárias — o perfil exato do produtor que este sistema pretende servir.

- **Um terço da renda anual em 75 dias.** Reportagem da Secretaria do Desenvolvimento Sustentável do Paraná documenta o caso de **Elizabeth Guedes de Freitas Costa, produtora de Campina Grande do Sul** — exatamente uma das duas cidades-alvo deste projeto. Para a família dela, o pinhão representa **um terço da renda do ano inteiro**, concentrado nos cerca de **75 dias** da janela legal de safra (15/04 a 30/06, IAT nº 03/2026). Fora dessa janela, são mais de 80% do ano sem receita direta dessa cadeia.

- **Pequeno no agregado nacional, grande na região.** No conjunto dos produtos não-madeireiros do extrativismo brasileiro, o pinhão representa cerca de **3,3% do valor** — muito atrás do açaí (46%) e da erva-mate (31,8%). O número parece pouco porque é um mapa de distribuição: a cadeia do pinhão é **concentrada** em poucos estados e, dentro do Paraná, em poucas microrregiões, das quais a Rota do Pinhão (que inclui Campina Grande do Sul e Quatro Barras) é a principal.

Esse quadro explica por que um sistema simples de gestão faz diferença aqui: uma cadeia concentrada, com janela curta, totalmente extrativista e em árvore criticamente ameaçada — cada quilo registrado importa, tanto para a renda familiar quanto para a rastreabilidade ambiental.

## O problema, em termos práticos

Pequenos produtores extrativistas de pinhão do Primeiro Planalto Paranaense operam, em sua maioria, sem nenhum tipo de controle sistemático da produção. Toda a gestão é feita em cadernos, papéis avulsos ou na memória, o que gera quatro consequências diretas e recorrentes:

1. **Desconhecimento da produtividade real por safra.** Sem registrar kg colhidos por dia e por propriedade, o produtor não consegue avaliar se sua produção melhorou, estagnou ou caiu ao longo dos anos — e, portanto, não consegue negociar com cooperativa nem pleitear crédito rural com base em histórico.
2. **Ausência de histórico climático.** A produção da araucária é altamente sensível a temperatura, umidade e regime de chuvas. Uma safra fraca pode ser culpa de uma geada tardia ou de um outono muito seco, mas sem dados atrelados não há como saber — e não há como se planejar para o ano seguinte.
3. **Venda no momento errado.** O preço do pinhão oscila fortemente dentro da própria safra. Sem histórico de preços comparado à média, o produtor vende para o primeiro comprador que aparece, tipicamente um atravessador que passa na porteira em maio. Em muitos casos, esperar duas ou três semanas significaria 30–40% a mais no quilo.
4. **Perdas pós-colheita.** Pinhão é altamente perecível. Armazenado a granel, dura cerca de 30 dias; a vácuo refrigerado, até 120 dias; e congelado, até 210 dias. Sem controle do método e da data de entrada em estoque, produto vence dentro do armazém e vira prejuízo puro.

O **Pinhão Tracker** resolve essas quatro dores com cadastros estruturados, alertas automáticos de vencimento, validação do período oficial de safra e relatórios comparativos entre anos.

## Por que Campina Grande do Sul e Quatro Barras

Os dois municípios estão no coração da **Rota do Pinhão**, circuito turístico e gastronômico criado pelo governo do Paraná que reúne os pontos de maior concentração de araucárias nativas do estado. A região reúne três características que a tornam estratégica:

- **Altitude acima de 800 metros** na Serra do Mar paranaense, condição ideal para a *Araucaria angustifolia*.
- **Temperatura média anual entre 15 °C e 25 °C**, dentro da faixa ótima para a espécie.
- **Cooperativismo ativo**, com destaque para a **Cooperativa Nascente**, que agrega pequenos produtores extrativistas e reforça o papel do pinhão como fonte complementar de renda em propriedades familiares.

O extrativismo do pinhão é, nessas duas cidades, uma renda sazonal relevante em propriedades que combinam agricultura familiar, turismo rural e produção de erva-mate. Uma ferramenta de gestão simples reduz perdas pós-colheita, aumenta o poder de barganha em relação ao atravessador e gera histórico documental — ativo relevante tanto para acesso a crédito rural quanto para eventual rastreabilidade ambiental, dado que a espécie é criticamente ameaçada.

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

## Recurso extra: importação automática via API Open-Meteo

Além da importação por arquivo `.txt` (que cumpre integralmente o requisito de manipulação de `.txt`), o sistema oferece como **recurso opcional** a importação automática de histórico climático via **API pública da Open-Meteo** (serviço gratuito de dados meteorológicos, sem necessidade de chave de acesso).

### Por que esse extra existe

O produtor raramente tem estação meteorológica própria. Digitar clima dia a dia é inviável, e nem sempre há arquivo `.txt` pronto. Puxar o histórico da Open-Meteo por coordenada geográfica cobre essa lacuna e fecha o ciclo da segunda dor descrita no início deste documento (ausência de histórico climático atrelado à safra).

### Como funciona

1. No menu principal, entre em **3. Monitoramento Climatico**.
2. Escolha **3. Importar clima da API Open-Meteo (extra)**.
3. O sistema lista as propriedades cadastradas e pede o ID da propriedade-destino.
4. Exibe coordenadas de referência da região-alvo (Quatro Barras e Campina Grande do Sul) e pede latitude e longitude em graus decimais.
5. Pede data inicial e data final do período desejado.
6. Baixa temperatura média diária, umidade relativa média diária e precipitação total diária da API e grava na tabela `registros_climaticos` vinculada à propriedade.

### Sem bibliotecas externas adicionais

A integração usa apenas `urllib.request` e `json`, ambos da **biblioteca padrão do Python**. Nenhuma dependência a mais em relação ao projeto base — o requisito de usar apenas `oracledb` como biblioteca externa continua atendido.

### Fallback gracioso

Se a rede estiver indisponível, a API estiver fora do ar, ou o tempo limite for excedido, o sistema exibe mensagem clara e sugere a alternativa por arquivo `.txt`. Nenhum registro parcial é gravado em caso de falha de comunicação.

### Como desativar

Em `config.json`, no bloco `api_clima`, troque `"habilitada": true` para `"habilitada": false`. A opção some na prática: ao ser chamada, informa que o recurso está desativado e retorna ao menu.

### Atribuição

Os dados vêm do serviço **Open-Meteo** (<https://open-meteo.com>), sob licença **Creative Commons Attribution 4.0 (CC BY 4.0)**. A atribuição é exibida na tela do terminal toda vez que o recurso é utilizado.

### Configuração

```json
"api_clima": {
  "habilitada": true,
  "url_base": "https://archive-api.open-meteo.com/v1/archive",
  "timeout_segundos": 15,
  "atribuicao": "Dados climaticos de Open-Meteo (open-meteo.com) - licenca CC BY 4.0"
}
```

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
    ├── api_clima.py             # Cliente HTTP Open-Meteo (recurso extra)
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

## Fontes dos dados citados

- **Produção da Extração Vegetal e da Silvicultura (PEVS)** — IBGE, edições 2021 e 2023. Fornece volume, valor de produção e ranking estadual do pinhão: <https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/9105-producao-da-extracao-vegetal-e-da-silvicultura.html>
- **Pinhão e renda sazonal de pequenos produtores (caso Campina Grande do Sul)** — Secretaria do Desenvolvimento Sustentável do Paraná: <https://www.sedest.pr.gov.br/Noticia/No-Parana-pinhao-gera-renda-para-pequenos-produtores>
- **Status de conservação da *Araucaria angustifolia*** — União Internacional para a Conservação da Natureza (IUCN) Red List; Fundação Grupo Boticário: <https://fundacaogrupoboticario.org.br/ameacada-floresta-com-araucarias-ainda-e-motivo-de-preocupacao/>
- **Remanescentes da Floresta com Araucárias no Paraná** — cobertura de aproximadamente 0,4% da área original, reportagem da Mongabay Brasil: <https://brasil.mongabay.com/2022/03/araucarias-em-rota-de-extincao-sao-cortadas-com-aval-dos-orgaos-publicos/>
- **Instrução Normativa IAT nº 03/2026** — Instituto Água e Terra (Paraná), período oficial de coleta do pinhão: 15 de abril a 30 de junho.
- **Política de Garantia de Preços Mínimos para produtos da Sociobiodiversidade (PGPM-Bio)** — Conab / Ministério da Agricultura. Preço mínimo do pinhão: R$ 3,66/kg.
