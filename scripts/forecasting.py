# forecasting.py
from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os


def prepare_data_for_prophet(df, time_column, volume_column):
    """
    Prepara os dados para serem usados pelo Prophet.
    Renomeia as colunas conforme o formato esperado pelo Prophet.
    """
    if time_column not in df.columns or volume_column not in df.columns:
        raise KeyError(f"As colunas '{time_column}' ou '{volume_column}' não existem no DataFrame.")

    # Renomear colunas para o formato esperado pelo Prophet
    df = df[[time_column, volume_column]].rename(columns={time_column: "ds", volume_column: "y"})
    return df

def forecast_search_volume(df, periods=30):
    """
    Executa previsões usando o modelo Prophet.
    """
    from prophet import Prophet

    # Inicializar o modelo Prophet
    model = Prophet()
    model.fit(df)

    # Criar datas futuras para previsão
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

def plot_forecast(forecast, original_data):
    """
    Plota a previsão gerada pelo Prophet junto com os dados originais
    e salva a figura automaticamente na pasta 'results'.
    """
    import os
    import matplotlib.pyplot as plt

    # Criar o diretório 'results' caso não exista
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))

    # Plotar os dados originais
    plt.plot(original_data["ds"], original_data["y"], label="Dados Originais", color="blue")

    # Plotar a previsão
    plt.plot(forecast["ds"], forecast["yhat"], label="Previsão", color="red")

    # Adicionar intervalo de confiança
    plt.fill_between(
        forecast["ds"],
        forecast["yhat_lower"],
        forecast["yhat_upper"],
        color="pink",
        alpha=0.3,
        label="Intervalo de Confiança"
    )

    # Configurações do gráfico
    plt.title("Previsão de Volume de Busca (Agregado)")
    plt.xlabel("Data")
    plt.ylabel("Volume de Busca (Média do Rank)")
    plt.legend()
    plt.grid(True)

    # Ajustar formatação do eixo x
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.gcf().autofmt_xdate(rotation=45)

    # Salvar a figura
    save_path = os.path.join(results_dir, "forecast_plot.png")
    plt.savefig(save_path)
    print(f"Gráfico salvo em: {save_path}")

    plt.show()
