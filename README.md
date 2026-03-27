# Análise de Dados para Políticas Públicas

Esta análise realizada com os microdados do ENEM 2023 em conjunto com os dados do Produto Interno Bruto (PIB) dos municípios brasileiros (IBGE, 2023). O objetivo principal é extrair insights que possam guiar políticas públicas, avaliando o impacto de fatores socioeconômicos, demográficos e regionais no desempenho acadêmico dos estudantes.

🌐 **Acesse a aplicação online:** [Dashboard ENEM no Streamlit](https://analysis-enem.streamlit.app/)  
_(Nota: Devido ao grande volume de dados, a aplicaçãom pode apresentar instabilidades.)._

---

## Como executar o projeto localmente

Para rodar o projeto na localmente, utilizaremos o `pyenv` para gerenciar a versão do Python e isolar as dependências do ambiente.

### 1. Preparando o Ambiente (Python 3.12)

Certifique-se de ter o `pyenv` instalado. Em seguida, execute os comandos abaixo no seu terminal:

```bash
pyenv install 3.12.13

# Crie um ambiente virtual (substitua 'enem-env' pelo nome que preferir)
pyenv virtualenv 3.12.13 enem-env

# Ative o ambiente virtual na pasta do projeto
pyenv local enem-env

# Se o comando acima não funcionar utilize (enem-env é o nome que você escolheu)
pyenv active enem-env

# Instale as bibliotecas necessárias
pip install -r requirements.txt
```

### 2. Download das Bases de Dados

Os dados brutos do ENEM e do IBGE são pesados (a base do ENEM possui cerca de 2GB) e não estão versionados no GitHub. Você precisará baixá-los manualmente:

1. **Microdados do ENEM 2023:** [Acesse o portal do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) e faça o download.
2. **PIB dos Municípios 2023:** [Acesse o portal do IBGE](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?t=downloads&c=1100031) e baixe a planilha.

**Estrutura de pastas:** Na raiz do projeto, crie a seguinte estrutura de diretórios e coloque os arquivos baixados dentro da pasta `raw`:

```text
├── data/
│   ├── raw/
│   │   ├── microdados-enem-2023.csv
│   │   └── pib-dos-municipios-2010-2023.xlsx
│   └── processed/
```

### 3. Processamento dos Dados

Devido ao tamanho das bases e para "facilitar" a hospedagem e a performance da análise, **os dados foram limitados na extração (cerca de 500.000 de linhas iniciais)**.

Para limpar, transformar e gerar os arquivos otimizados `.parquet`, execute:

```bash
python3 pipeline.py
```

_Este script irá ler os arquivos de `data/raw/`, aplicar os filtros (como remover treineiros, tratar valores nulos, calcular faixas de renda e mapear regiões) e salvar os resultados em `data/processed/`._

### 4. Executando o Dashboard

Com os dados prontos, inicie a aplicação Streamlit:

```bash
streamlit run main.py
```

O dashboard será aberto automaticamente no seu navegador padrão.

---

## _Insights_

### 1. Estatísticas Descritivas

- **O que pensei:** Antes de cruzar dados complexos, precisamos entender a "linha de base". Qual é a média geral das notas? Como está a dispersão (desvio padrão)?
- **Insight:** Essa tabela inicial serve para balizar a análise. Ela nos mostra rapidamente onde os alunos têm mais dificuldade (geralmente Ciências da Natureza ou Matemática) e onde a nota costuma ser mais alta ou ter mais variância (como na Redação).

### 2. Disparidades por Tipo de Escola (Pública x Privada)

- **O que pensei:** Uma das maiores discussões em políticas públicas educacionais é o abismo entre o ensino público e o privado. Decidi criar gráficos que mostrassem não apenas a proporção de alunos de cada rede, mas como a curva de notas se comporta para ambos.
- **Insight:** Nos histogramas de Matemática e Redação, fica visualmente claro o deslocamento da curva de notas da escola privada para a direita (notas mais altas), enquanto a curva da escola pública se concentra mais à esquerda.

### 3. Distribuição das Notas por Região e Gênero

- **O que pensei:** A desigualdade no Brasil é fortemente marcada por recortes geográficos e de gênero. Utilizei _Boxplots_ para analisar a variância das notas divididas pelas 5 regiões do Brasil e por sexo.
- **Insight:** O gráfico permite identificar as diferenças regionais (como a diferença de medianas entre Sudeste/Sul e Norte/Nordeste) e também avaliar se existe um viés de gênero no desempenho em áreas específicas, como exatas (Matemática/Natureza) versus humanas/linguagens.

### 4. Histograma Geral Segmentado

- **O que pensei:** Queria uma visualização fluida de densidade para entender onde a grande massa de estudantes está concentrada em cada área do conhecimento.
- **Insight:** Esta análise reforça a seção 2, mas de forma dinâmica. Ao selecionar diferentes matérias, podemos ver que disciplinas como Ciências Humanas tendem a ter uma distribuição mais "normal", enquanto Matemática apresenta uma assimetria forte para notas mais baixas na rede pública.

### 5. Matriz de Correlação das Notas

- **O que pensei:** Um aluno que vai bem em Matemática também vai bem em Redação? Para responder isso, gerei um _Heatmap_ com as correlações de Pearson entre todas as provas.
- **Insight:** Normalmente, vemos uma correlação mais forte entre Ciências Humanas e Linguagens, e entre Ciências da Natureza e Matemática. A Redação costuma ter um comportamento um pouco mais isolado.

### 6. Impacto Socioeconômico

- **O que pensei:** O desempenho acadêmico é um reflexo do ambiente financeiro? Decidi cruzar os microdados do ENEM (agrupados por município) com o **PIB per capita** do IBGE e a **Renda Média Familiar** declarada pelos alunos. Como prova de conceito, foquei nos municípios de Minas Gerais (como São João del-Rei, Ouro Branco, Belo Horizonte, etc.).
- **Insight:** Através do _Heatmap_ de correlação socioeconômica, podemos validar matematicamente se municípios mais ricos (maior PIB) entregam, de fato, alunos com melhor desempenho, ou se o fator determinante principal é, na verdade, a Renda Familiar microeconômica do indivíduo. Mas como resultado não obtive uma correlação direta.

## Limitações

- **Volume de Dados e Amostragem:** A base bruta de microdados do ENEM 2023 é extremamente densa (cerca de 2 GB de dados). Para viabilizar o processamento localmente e permitir o deploy gratuito, foi necessário limitar a leitura da base de dados. Logo, o dashboard trabalha com uma amostra representativa dos dados originais.

- **Instabilidade no _Streamlit_:** Como consequência direta do volume de dados, a hospedagem pode apresentar instabilidades. Mesmo com os dados limitados `.parquet`, operações de filtragem dinâmica e renderização de gráficos tendem a consumir muita memória, o que pode fazer a aplicação falhar ou reiniciar.

- **Baixa Correlação com o PIB:** A hipótese inicial de que o PIB municipal teria uma correlação direta e forte com as notas médias do ENEM não se confirmou da maneira esperada. Para obter correlações mais precisas sobre o impacto na educação, seria necessário utilizar outros indicadores, como o Índice de Gini (desigualdade) ou o IDHM (Índice de Desenvolvimento Humano Municipal).
