import pandas as pd
import numpy as np
def feature_engineering(df:pd.DataFrame):
    '''
        Aplica técnicas de feature engineering para criação de variáveis derivadas
        utilizadas na análise e modelagem dos dados.
    '''
    max_projetos = df['projetos'].max() if df['projetos'].max() > 0 else 1
    max_meses = df['meses_estudo'].max() if df['meses_estudo'].max() > 0 else 1


    #------------------------------------------
    # # 1. Cálculo da taxa de conversão (% entrevistas / candidaturas)
    #------------------------------------------
    df['conversao_percentual']=np.where(
        df['candidaturas']>0,
        round((df['entrevistas']/df['candidaturas'])*100,1),
        0.0
    )

    #------------------------------------------
    # 2. Criação de variável categórica de nível de experiência baseada em tempo de estudo
    #------------------------------------------
    bins = [-0.1, 6, 18, 36, np.inf]
    labels = ['Iniciante (<6m)', 'Intermediário (6-18m)', 'Avançado (18-36m)', 'Sênior (36m+)']
    df['nivel_experiencia'] = pd.cut(df['meses_estudo'], bins=bins, labels=labels, include_lowest=True)

    #------------------------------------------
    # 3. Classificação da eficiência na busca com base na taxa de conversão
    #------------------------------------------
    conditions = [
        df['conversao_percentual'] == 0,
        (df['conversao_percentual'] > 0) & (df['conversao_percentual'] <= 10),
        (df['conversao_percentual'] > 10) & (df['conversao_percentual'] <= 25),
        df['conversao_percentual'] > 25
    ]
    choices=['Sem entrevistas', 'Baixa (0-10%)', 'Média (10-25%)', 'Alta (>25%)']
    df['eficiencia_busca'] = np.select(conditions, choices, default='Média')

    #------------------------------------------
    # 4. Cálculo de score de preparação técnica normalizado (0-100)
    #------------------------------------------
    df['score_preparacao'] = (
        (df['projetos'] / max_projetos * 40) +
        (df['meses_estudo'] / max_meses * 30) +
        (df['peso_cursos'] / 5 * 30)
    ).round(1).clip(upper=100)


    #------------------------------------------
    # 5. Cálculo da intensidade de busca (candidaturas por mês de estudo)
    #------------------------------------------
    df['intensidade_busca'] = np.where(
        df['meses_estudo'] > 0, 
        round(df['candidaturas'] / df['meses_estudo'], 2), 
        0
    )

    #------------------------------------------
    #  6. Cálculo do score de adaptação à IA baseado na percepção de dificuldade e portfólio
    #------------------------------------------
    df['score_adaptacao_ia'] = (
        ((5 - df['dificuldade_ia']) / 4 * 60) + 
        (df['projetos'] / max_projetos * 40)
    ).round(1).clip(upper=100)

    #------------------------------------------
    # 7. Classificação categórica da empregabilidade com base no score de preparação
    #------------------------------------------

    bins_emp = [-0.1, 30, 55, 75, 100]
    labels_emp = ['Crítica', 'Em Desenvolvimento', 'Boa', 'Excelente']
    df['classificacao_empregabilidade'] = pd.cut(df['score_preparacao'], bins=bins_emp, labels=labels_emp, include_lowest=True)

    return df