# data_cleaning.py
import pandas as pd

def clean_data(df):
    """
    Realiza a limpeza básica nos dados:
    - Remove valores nulos.
    - Renomeia as colunas para os nomes esperados.
    - Verifica se as colunas obrigatórias existem.
    - Agrega os dados por dia para evitar duplicações.
    """
    # Remover valores nulos
    df = df.dropna()

    # Renomear colunas para os nomes esperados
    rename_map = {
        'Day': 'day',
        'Term': 'term',
        'Score': 'score',
        'Rank': 'rank',
        'State': 'state'
    }
    df = df.rename(columns=rename_map)

    # Verificar se as colunas obrigatórias existem
    required_columns = ['day', 'term', 'score', 'rank', 'state']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Coluna obrigatória ausente: {col}")

    # Agregar dados por dia e estado (média de score por dia e estado)
    df = df.groupby(['day', 'state'], as_index=False)['score'].mean()

    return df

def convert_dates(df, date_column):
    """
    Converte a coluna de datas para o formato datetime.
    """
    if date_column not in df.columns:
        raise KeyError(f"Coluna de data '{date_column}' não encontrada no DataFrame.")

    df[date_column] = pd.to_datetime(df[date_column])
    return df

def normalize_categories(df, category_column):
    """
    Normaliza os valores de uma coluna categórica para minúsculas.
    """
    if category_column not in df.columns:
        raise KeyError(f"Coluna categórica '{category_column}' não encontrada no DataFrame.")

    df[category_column] = df[category_column].str.lower()
    return df
