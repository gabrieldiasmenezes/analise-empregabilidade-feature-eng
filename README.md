# 📊 Sistema de Análise de Empregabilidade em Tecnologia

**Disciplina:** Modelagem Linear para Aprendizado de Máquina  
**Instituição:** FIAP  
**Período:** 2026  

---

## � Integrantes do Projeto

| # | Nome | RM |
|---|---|---|
| 1 | Bruna Yukimy Hada | RM 571836 |
| 2 | Denize Ferrante | RM 571562 |
| 3 | Gabriel Dias Menezes | RM 572395  |
| 4 | Jeferson dos Santos Oliveira | RM 572594 |
| 5 | Kayki Muran do Nascimento Yamauchi | RM572466 |

---

## �📋 Descrição do Projeto

Este projeto desenvolve uma **base de dados fictícia realista** que simula um sistema de pesquisa sobre empregabilidade e preparação profissional de tecnólogos em formação. Os dados foram coletados via **formulário online** e processados através de validação, limpeza e engenharia de atributos (feature engineering) utilizando Python.

O objetivo é criar um conjunto de dados estruturado que represente informações reais de candidatos à tecnologia, incluindo:
- Situação profissional atual
- Formação e experiência técnica
- Percepção de desafios (IA e mercado)
- Atividades de busca por emprego
- Impacto de mentoria profissional

A base de dados final é exportada para **formato Excel (.xlsx)** após validação completa.

---

## 🎯 Requisitos Acadêmicos Atendidos

✅ **Requisito 01:** Base de dados fictícia gerada em Python  
✅ **Requisito 02:** Exportação em formato .xlsx  
✅ **Mínimo de 100 linhas** de dados  
✅ **Mínimo de 15 colunas** após engenharia de atributos  
✅ **Múltiplos tipos de dados:** Categóricos e Numéricos  
✅ **Validação de dados** implementada  
✅ **Coerência e consistência** com contexto de empregabilidade  

---

## 📁 Estrutura do Projeto

```
cp2/
├── main.py                          # Script principal de orquestração
├── requirements.txt                 # Dependências do projeto
├── README.md                        # Este arquivo
├── database.xlsx                    # Saída: Base de dados processada (Excel)
├── data/
│   └── data.csv                     # Dados brutos do formulário
└── src/
    ├── clean_data.py                # Módulo de limpeza e validação
    ├── feature_engineering.py       # Módulo de engenharia de atributos
    └── __pycache__/                 # Cache do Python
```

---

## 📊 Descrição da Base de Dados

### Origem dos Dados
A base de dados foi gerada através de um **formulário online** que coletou informações sobre:
- Perfil profissional de tecnólogos em formação
- Experiência e educação
- Percepção sobre IA e dificuldade no mercado
- Atividades de busca por emprego
- Relacionamento com mentores profissionais

### Dimensões
- **Linhas:** 100+ registros de respondentes
- **Colunas:** 19 atributos (originais + derivados)
- **Tipos de Dados:** Numéricos, Categóricos, Percentuais

---

## 🔄 Pipeline de Processamento

### 1️⃣ **Carregamento dos Dados**
```python
df = pd.read_csv('data/data.csv')
```
Leitura do arquivo CSV contendo as respostas brutas do formulário.

### 2️⃣ **Limpeza de Dados** (`clean_data.py`)

#### ✨ Etapa 1: Limpeza Básica
- Remoção de espaços em branco nos nomes das colunas
- Exclusão de colunas administrativas:
  - `Hora de início`, `Hora de conclusão`
  - `Email`, `Nome`, `Hora da última modificação`

#### 🔤 Etapa 2: Padronização de Nomes
Renomeia colunas do formulário para nomes padronizados em minúsculas:

| Coluna Original | Coluna Padronizada |
|---|---|
| ID | id |
| Qual sua situação atual na área de tecnologia? | situacao |
| Qual é a sua principal formação atual? | formacao |
| ... | ... |

#### 🔢 Etapa 3: Conversão Numérica
Converte coluna para tipo numérico com tratamento de erros:
```python
numeric_cols = ['meses_estudo', 'peso_diploma', 'peso_cursos', 'projetos', ...]
df[col] = pd.to_numeric(df[col], errors='coerce')
```

#### ✅ Etapa 4: Validação Lógica
- **Valores negativos:** Corrigidos com `clip(lower=0)`
  - `projetos`, `candidaturas`, `entrevistas`, `meses_estudo`
- **Faixas de escala (1-5):** Garantidas com `clip(lower=1, upper=5)`
  - `peso_diploma`, `peso_cursos`, `dificuldade_ia`, `impacto_mentoria`
- **Regra de negócio:** Se `mentor = 'Não'`, então `impacto_mentoria = 0`

#### 🔧 Etapa 5: Imputação de Valores Ausentes
Preenchimento pela mediana (robustez a outliers):
```python
df[col] = df[col].fillna(df[col].median())
```

### 3️⃣ **Feature Engineering** (`feature_engineering.py`)

Criação de 7 novos atributos derivados para enriquecer análises:

#### 📈 **conversao_percentual**
Taxa de conversão de candidaturas em entrevistas:

- **Tipo:** Numérico (%)
- **Range:** 0 a 100%

#### 📊 **nivel_experiencia**
Categorização baseada em meses de estudo:
| Faixa | Categoria |
|---|---|
| < 6 meses | Iniciante (<6m) |
| 6-18 meses | Intermediário (6-18m) |
| 18-36 meses | Avançado (18-36m) |
| > 36 meses | Sênior (36m+) |

#### 🎯 **eficiencia_busca**
Classificação da eficácia da busca por emprego:
| Conversão | Classificação |
|---|---|
| 0% | Sem entrevistas |
| 0-10% | Baixa (0-10%) |
| 10-25% | Média (10-25%) |
| > 25% | Alta (>25%) |

#### ⭐ **score_preparacao**
Score técnico normalizado de 0 a 100:


**Composição:**
- Portfólio (projetos): 40%
- Experiência (tempo): 30%
- Formação contínua (cursos): 30%

#### 💨 **intensidade_busca**
Candidaturas por mês de estudo ativo:

- **Unidade:** vagas/mês
- Indica o ritmo de busca por emprego

#### 🤖 **score_adaptacao_ia**
Score de adaptação à IA baseado em percepção e portfólio:


**Componentes:**
- Resiliência (inverso da dificuldade percebida): 60%
- Experiência prática (portfólio): 40%

#### 🏆 **classificacao_empregabilidade**
Categoria de empregabilidade baseada no score de preparação:

| Score | Classificação |
|---|---|
| 0-30 | Crítica |
| 30-55 | Em Desenvolvimento |
| 55-75 | Boa |
| 75-100 | Excelente |

### 4️⃣ **Organização Final**
Seleção de 19 colunas para exportação:
```python
final_cols = [
    'id', 'situacao', 'formacao', 'nivel_experiencia', 'meses_estudo',
    'peso_diploma', 'peso_cursos', 'projetos', 'score_preparacao',
    'dificuldade_ia', 'score_adaptacao_ia', 'candidaturas', 'entrevistas',
    'conversao_percentual', 'eficiencia_busca', 'intensidade_busca',
    'mentor', 'impacto_mentoria', 'classificacao_empregabilidade'
]
```

### 5️⃣ **Exportação**
Salvamento em formato Excel:
```python
df.to_excel('database.xlsx', index=False)
```

---

## 📑 Dicionário de Dados

| # | Coluna | Tipo | Range/Valores | Descrição |
|---|---|---|---|---|
| 1 | **id** | int | 1-N | Identificador único do respondente |
| 2 | **situacao** | string | Estudante, Profissional, Desempregado | Situação atual na área de tecnologia |
| 3 | **formacao** | string | Faculdade, Bootcamp, Autodidata | Principal formação atual |
| 4 | **nivel_experiencia** | string | Iniciante, Intermediário, Avançado, Sênior | Nível baseado em tempo de estudo |
| 5 | **meses_estudo** | int | 0-120+ | Meses de estudo ativo em tecnologia |
| 6 | **peso_diploma** | int | 1-5 | Importância do diploma faculdade (1=baixo, 5=alto) |
| 7 | **peso_cursos** | int | 1-5 | Importância de cursos/bootcamps (1=baixo, 5=alto) |
| 8 | **projetos** | int | 0-100+ | Quantidade de projetos no portfólio |
| 9 | **score_preparacao** | float | 0-100 | Score de preparação técnica (derivado) |
| 10 | **dificuldade_ia** | int | 1-5 | Percepção de aumento de dificuldade por IA |
| 11 | **score_adaptacao_ia** | float | 0-100 | Score de adaptação à IA (derivado) |
| 12 | **candidaturas** | int | 0-1000+ | Vagas que se candidatou (últimos 3 meses) |
| 13 | **entrevistas** | int | 0-500+ | Entrevistas obtidas (últimos 3 meses) |
| 14 | **conversao_percentual** | float | 0-100 | Taxa de conversão (derivada) |
| 15 | **eficiencia_busca** | string | Sem entrevistas, Baixa, Média, Alta | Classificação da eficiência (derivada) |
| 16 | **intensidade_busca** | float | 0-50+ | Candidaturas por mês (derivada) |
| 17 | **mentor** | string | Sim, Não | Possui ou teve mentor profissional |
| 18 | **impacto_mentoria** | float | 0-5 | Impacto da mentoria na evolução |
| 19 | **classificacao_empregabilidade** | string | Crítica, Em Desenvolvimento, Boa, Excelente | Classificação final (derivada) |

---

## 🚀 Como Executar

### 📋 Pré-requisitos
- **Python 3.8+** instalado
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para controle de versão)

### 📂 Passo 1: Clonar ou Baixar o Projeto

```bash
# Opção 1: Clonar do repositório (se aplicável)
git clone <URL_DO_REPOSITORIO>
cd cp2

# Opção 2: Ou simplesmente acesse a pasta do projeto
cd c:\Users\Administrador\Desktop\MyArea\2026\fiap\modelagemLinear\cp2
```

### 🔧 Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# No Windows (CMD):
venv\Scripts\activate.bat

# No Linux/Mac:
source venv/bin/activate
```

### 📦 Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências instaladas:**
- `pandas==3.0.2` - Manipulação e análise de dados
- `numpy==2.4.4` - Operações numéricas e arrays
- `openpyxl==3.1.5` - Leitura e escrita de arquivos Excel
- `python-dateutil==2.9.0.post0` - Manipulação de datas
- `six==1.17.0` - Compatibilidade Python 2/3
- `tzdata==2026.1` - Dados de fuso horário
- `et_xmlfile==2.0.0` - Suporte XML para Excel

### ▶️ Passo 4: Executar o Pipeline Completo

```bash
python main.py
```

**Saída esperada:**
```
📥 Dataset carregado: 100 linhas | 18 colunas

Base validada e exportada com sucesso!
Linhas finais: 100 | Colunas finais: 19
Novas colunas adicionadas para apresentação:
    conversao_percentual (%)
    nivel_experiencia (Categórico)
    eficiencia_busca (Categórico)
    score_preparacao (0-100)
    intensidade_busca (vagas/mês)
    score_adaptacao_ia (0-100)
    classificacao_empregabilidade (Categórico)
```

### 📊 Passo 5: Acessar o Arquivo de Saída

Após a execução bem-sucedida, o arquivo será criado na raiz do projeto:

📁 **`database.xlsx`** - Base de dados processada e validada

**Abrir o arquivo:**
- **Excel:** Duplo clique em `database.xlsx`
- **Python (para análise programática):**
  ```python
  import pandas as pd
  df = pd.read_excel('database.xlsx')
  print(df.head())
  print(df.info())
  ```

### 🐛 Solução de Problemas

| Problema | Solução |
|---|---|
| `ModuleNotFoundError` | Execute `pip install -r requirements.txt` novamente |
| `FileNotFoundError: data/data.csv` | Certifique-se que o arquivo `data/data.csv` existe |
| Ambiente virtual não ativa | Use o caminho completo: `venv\Scripts\Activate.ps1` (PowerShell) |
| Excel não se abre | Instale Excel ou use `LibreOffice Calc` |

### 💡 Dicas de Uso

✅ **Integre ao seu workflow:**
```bash
# Executar periodicamente
python main.py
```

✅ **Modificar dados de entrada:**
Edite ou substitua o arquivo `data/data.csv` com novos dados

✅ **Debug e inspeção:**
```python
# Adicione ao final do main.py para inspecionar dados intermediários
print(df.describe())  # Estatísticas descritivas
print(df.dtypes)     # Tipos de dados
print(df.isnull().sum())  # Valores ausentes
```

### ✨ Próximas Etapas

Com a base de dados gerada (`database.xlsx`), você pode:
1. Importar em ferramentas de BI (Power BI, Tableau)
2. Realizar análises estatísticas (R, Python scipy/statsmodels)
3. Treinar modelos de Machine Learning (scikit-learn, tensorflow)
4. Criar visualizações (matplotlib, seaborn, plotly)

---

## 🔍 Detalhes Técnicos

### Validações Implementadas

1. **Tipo de Dados:** Conversão e coerção de tipos
2. **Ranges:** Clipping de valores fora da faixa esperada
3. **Valores Ausentes:** Imputação pela mediana
4. **Regras de Negócio:** Relacionamentos entre variáveis (ex: mentor → impacto)
5. **Consistência Lógica:** Valores negativos corrigidos
6. **Normalização:** Score padronizados de 0-100

### Decisões de Design

| Decisão | Justificativa |
|---|---|
| Imputação pela mediana | Robusta a outliers, mantém distribuição |
| Clipping vs Exclusão | Preserva registros, corrige extremos implausíveis |
| Feature Engineering | Enriquece análise com métricas derivadas relevantes |
| Categorização | Facilita interpretação e análise segmentada |
| Normalização 0-100 | Comparabilidade entre scores heterogêneos |

---

## 📊 Possíveis Análises

Com a base de dados estruturada, é possível realizar:

- 📈 **Análise Descritiva:** Perfil dos respondentes, distribuições
- 🔗 **Correlações:** Relações entre preparação e sucesso na busca
- 🎯 **Segmentação:** Grupos por nível de experiência, eficiência
- 🤖 **Modelagem:** Previsão de empregabilidade usando Regressão Linear
- 📊 **Visualização:** Gráficos de distribuições, heatmaps de correlação
- 🔮 **Previsão:** Scores e classificações automáticas

---

## 🛠️ Estrutura de Código

### `main.py`
Orquestrador principal que executa todo o pipeline em sequência.

### `src/clean_data.py`
Funçã `clean_dataset(df)` que realiza validação e limpeza completa dos dados.

### `src/feature_engineering.py`
Função `feature_engineering(df)` que cria atributos derivados.

---

## 📌 Notas Importantes

- ✅ Base de dados é **100% fictícia** mas **realista** em contexto
- ✅ Todos os dados foram **validados** e **normalizados**
- ✅ Pipeline é **automatizado** e **reproduzível**
- ✅ Código segue **boas práticas** de Python
- ✅ Exportação em **formato Excel** padrão (.xlsx)

---

## 👥 Informações Adicionais

**Contexto da Pesquisa:** Empregabilidade de tecnólogos em era de IA  
**Público-Alvo:** Estudantes e profissionais em transição para tecnologia  
**Período de Coleta:** 2026  
**Coerência:** Base representa realidade atual do mercado de tecnologia  

---

**Última atualização:** April 2026  
**Status:** ✅ Completo e validado
