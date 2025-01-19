from scripts.bigquery_connector import fetch_data
from scripts.data_cleaning import clean_data
from scripts.forecasting import prepare_data_for_prophet, forecast_search_volume, plot_forecast
import pandas as pd
import os

def main():
    from dotenv import load_dotenv # type: ignore

    # Carregar variáveis do .env
    load_dotenv()

    # Obter a query do .env
    query = os.getenv("BIGQUERY_SQL")
    location = os.getenv("LOCATION")

    if not query:
        raise ValueError("Query SQL não encontrada no arquivo .env")

    # Conectar e obter dados
    print("Buscando dados do BigQuery...")
    data = fetch_data(query, location)

    # Salvar dados brutos
    raw_file_path = "data/raw/full_top_terms.csv"
    os.makedirs("data/raw", exist_ok=True)
    data.to_csv(raw_file_path, index=False)
    print(f"Dados salvos em {raw_file_path}")

    print("Limpando dados...")
    cleaned_data = clean_data(data)

    # Criar o diretório, se necessário
    os.makedirs("data/processed", exist_ok=True)

    # Dividir os dados por estado
    for state in cleaned_data['state'].unique():
        state_data = cleaned_data[cleaned_data['state'] == state]
        state_file_path = f"data/processed/cleaned_data_{state}.csv"
        state_data.to_csv(state_file_path, index=False)
        print(f"Dados limpos salvos para o estado {state}: {state_file_path}")

    # Salvar a visão nacional
    national_file_path = "data/processed/cleaned_data_national.csv"
    national_data = cleaned_data.groupby('day', as_index=False)['score'].mean()
    national_data.to_csv(national_file_path, index=False)
    print(f"Dados limpos salvos para visão nacional: {national_file_path}")

    # Exibir informações gerais do DataFrame limpo
    print("Colunas no DataFrame limpo:")
    print(cleaned_data.columns)
    print(cleaned_data.head())

    # Preparar previsões para estados e visão nacional
    print("Preparando previsões por estado e visão nacional...")

    for state in cleaned_data['state'].unique():
        state_data = cleaned_data[cleaned_data['state'] == state]
        print(f"Preparando previsão para o estado: {state}")

        # Previsão por estado
        prophet_data_state = prepare_data_for_prophet(state_data, time_column="day", volume_column="score")
        forecast_data_state = forecast_search_volume(prophet_data_state, periods=30)

        # Salvar previsão do estado
        state_forecast_path = f"data/processed/forecast_{state}.csv"
        forecast_data_state.to_csv(state_forecast_path, index=False)
        print(f"Previsão salva para o estado {state}: {state_forecast_path}")

    # Previsão para visão nacional
    print("Preparando previsão para visão nacional...")
    prophet_data_national = prepare_data_for_prophet(national_data, time_column="day", volume_column="score")
    forecast_data_national = forecast_search_volume(prophet_data_national, periods=30)

    # Salvar previsão nacional
    national_forecast_path = "data/processed/forecast_national.csv"
    forecast_data_national.to_csv(national_forecast_path, index=False)
    print(f"Previsão salva para visão nacional: {national_forecast_path}")

    # Exibir exemplo de previsão nacional no console
    print(forecast_data_national.head())

    # Exibir gráfico de previsão nacional
    print("Plotando previsão nacional...")
    plot_forecast(forecast_data_national, prophet_data_national)

if __name__ == "__main__":
    main()
