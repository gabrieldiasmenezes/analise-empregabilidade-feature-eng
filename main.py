import os
import pandas as pd
import numpy as np
from src.clean_data import clean_dataset
from src.feature_engineering import feature_engineering
os.system('cls')

def main():
    #------------------------------------------
    # 1. Carregamento dos dados
    #------------------------------------------
    df = pd.read_csv('data/data.csv')
    print(f"📥 Dataset carregado: {len(df)} linhas | {len(df.columns)} colunas")

    #------------------------------------------
    # 2. Limpeza dos dados
    #------------------------------------------
    df=clean_dataset(df)

    #------------------------------------------
    # 3. Inserção das Features Engineering
    #------------------------------------------
    df=feature_engineering(df)

    #------------------------------------------
    # 4. Organização Final para o Excel
    #------------------------------------------
    final_cols = [
        'id', 'situacao', 'formacao', 'nivel_experiencia', 'meses_estudo',
        'peso_diploma', 'peso_cursos', 'projetos', 'score_preparacao',
        'dificuldade_ia', 'score_adaptacao_ia', 'candidaturas', 'entrevistas',
        'conversao_percentual', 'eficiencia_busca', 'intensidade_busca',
        'mentor', 'impacto_mentoria', 'classificacao_empregabilidade'
    ]
    df = df[[col for col in final_cols if col in df.columns]]

    #------------------------------------------
    # 5. Exportando os Dados
    #------------------------------------------
    df.to_excel('database.xlsx', index=False)

    print(f"""
Base validada e exportada com sucesso!
Linhas finais: {len(df)} | Colunas finais: {len(df.columns)}
Novas colunas adicionadas para apresentação:
    conversao_percentual (%)
    nivel_experiencia (Categórico)
    eficiencia_busca (Categórico)
    score_preparacao (0-100)
    intensidade_busca (vagas/mês)
    score_adaptacao_ia (0-100)
    classificacao_empregabilidade (Categórico)
""")
    
if __name__=="__main__":
    main()