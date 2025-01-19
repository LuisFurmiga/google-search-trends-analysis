# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def load_forecast_data(state):
    """
    Carrega os dados de previsão gerados pelo Prophet para o estado selecionado.
    """
    try:
        if state == "Nacional":
            return pd.read_csv("data/processed/forecast_national.csv")
        else:
            return pd.read_csv(f"data/processed/forecast_{state}.csv")
    except FileNotFoundError:
        st.error(f"Dados de previsão para {state} não encontrados. Execute o pipeline para gerar os dados.")
        return None

def load_cleaned_data(state):
    """
    Carrega os dados limpos previamente salvos para o estado selecionado.
    """
    try:
        if state == "Nacional":
            return pd.read_csv("data/processed/cleaned_data_national.csv")
        else:
            return pd.read_csv(f"data/processed/cleaned_data_{state}.csv")
    except FileNotFoundError:
        st.error(f"Dados limpos para {state} não encontrados.")
        return None

def load_raw_data():
    """
    Carrega os dados brutos para visualização adicional.
    """
    try:
        return pd.read_csv("data/raw/full_top_terms.csv")
    except FileNotFoundError:
        st.error("O arquivo de dados brutos não foi encontrado. Execute o pipeline para gerar os dados.")
        return None

def plot_top_terms(data, top_n=10):
    """
    Plota os termos mais frequentes com base na contagem no dataset bruto.
    """
    top_terms = data['Term'].value_counts().head(top_n)
    plt.figure(figsize=(10, 6))
    top_terms.plot(kind='bar', color='skyblue')
    plt.title(f"Top {top_n} Termos Mais Frequentes")
    plt.xlabel("Termo")
    plt.ylabel("Frequência")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def plot_forecast(forecast, original_data):
    """
    Plota a previsão gerada pelo Prophet junto com os dados originais.
    """
    forecast["ds"] = pd.to_datetime(forecast["ds"], errors="coerce")
    original_data["ds"] = pd.to_datetime(original_data["day"], errors="coerce")

    plt.figure(figsize=(10, 6))

    # Plotar os dados originais
    plt.plot(original_data["ds"], original_data["score"], label="Dados Originais", color="blue")

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

    plt.title("Previsão de Volume de Busca")
    plt.xlabel("Data")
    plt.ylabel("Volume de Busca")
    plt.legend()
    plt.grid(True)

    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.gcf().autofmt_xdate(rotation=45)

    st.pyplot(plt)

def main():
    st.title("Análise de Tendências do Google Trends por Estado")

    # Carregar os estados disponíveis
    raw_data = load_raw_data()
    if raw_data is not None:
        states = raw_data['State'].unique().tolist()
        states.insert(0, "Nacional")

        # Seleção do estado
        selected_state = st.sidebar.selectbox("Selecione o Estado", states)

        # Carregar dados para o estado selecionado
        cleaned_data = load_cleaned_data(selected_state)
        forecast_data = load_forecast_data(selected_state)

        if cleaned_data is not None:
            st.subheader(f"Dados Limpos - {selected_state}")
            st.dataframe(cleaned_data.head(20))

        if forecast_data is not None:
            st.subheader(f"Gráfico de Previsão - {selected_state}")
            plot_forecast(forecast_data, cleaned_data)

if __name__ == "__main__":
    main()
