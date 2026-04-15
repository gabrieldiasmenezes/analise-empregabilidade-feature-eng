import pandas as pd

def clean_dataset(df:pd.DataFrame):

    '''
        Função que faz a validação dos dados do dataset importado e retorna um DataFrame validado e limpo
    '''

    #------------------------------------------
    # 1. LIMPEZA BÁSICA
    #------------------------------------------

    # Remoção de espaços em branco nos nomes das colunas
    df.columns=df.columns.str.strip()

    # Remoção de colunas administrativas e não relevantes para análise
    irrelevant_cols= ['Hora de início', 'Hora de conclusão', 'Email', 'Nome', 'Hora da última modificação']
    df = df.drop(columns=irrelevant_cols, errors='ignore')

    #------------------------------------------
    # 2. PADRONIZAÇÃO DE NOMES
    #------------------------------------------
    column_mapping = {
    'ID': 'id',
    'Qual sua situação atual na área de tecnologia?': 'situacao',
    'Qual é a sua principal formação atual?': 'formacao',
    'Há quantos meses você estuda tecnologia ativamente?': 'meses_estudo',
    'De 1 a 5, qual o peso do DIPLOMA FACULDADE na sua contratação?': 'peso_diploma',
    'De 1 a 5, qual o peso de CURSOS EXTRAS/BOOTCAMPS na sua contratação?': 'peso_cursos',
    'Quantos projetos práticos você tem no seu portfólio (GitHub, Behance, etc.)': 'projetos',
    'De 1 a 5, quanto você acredita que a IA aumentou a dificuldade de entrada?': 'dificuldade_ia',
    'Quantas vagas você já se candidatou nos últimos 3 meses?': 'candidaturas',
    'Quantas entrevistas você conseguiu nos últimos 3 meses?': 'entrevistas',
    'Você possui ou já possuiu um mentor na área?': 'mentor',
    'De 1 a 5, qual foi o impacto da mentoria na sua evolução?': 'impacto_mentoria'
    }
    df = df.rename(columns=column_mapping)

    #------------------------------------------
    # 3. CONVERSÃO NUMÉRICA
    #------------------------------------------
    numeric_cols = ['meses_estudo', 'peso_diploma', 'peso_cursos', 'projetos', 'dificuldade_ia', 'candidaturas', 'entrevistas', 'impacto_mentoria']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    #------------------------------------------
    # 4. VALIDAÇÃO LÓGICA
    #------------------------------------------

    # Correção de valores negativos em variáveis quantitativas
    for col in ['projetos', 'candidaturas', 'entrevistas', 'meses_estudo']:
        df[col] = df[col].clip(lower=0)
    
    # Garantindo faixas de 1 a 5 para avaliações
    for col in ['peso_diploma', 'peso_cursos', 'dificuldade_ia', 'impacto_mentoria']:
        df[col]=df[col].clip(lower=1,upper=5)

    # Aplicação de regra de negócio: usuários sem mentor não possuem impacto de mentoria
    df['mentor'] = df['mentor'].fillna('Não').str.strip()
    df.loc[df['mentor'] == 'Não', 'impacto_mentoria'] = 0

    #------------------------------------------
    # 5. Tratamento de valores ausentes via imputação pela mediana (robusto a outliers)
    #------------------------------------------
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    return df
