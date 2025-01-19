# Google Search Trends Analysis

## Descrição do Projeto
Este projeto realiza a análise de tendências de busca no Google com base em dados públicos do Google BigQuery. Ele utiliza o framework Prophet para gerar previsões de tendências, visualiza os dados em gráficos interativos e permite a análise por estado ou nacionalmente.

## Estrutura do Projeto

```
google-search-trends-analysis/
├── data/
│   ├── raw/              # Dados brutos coletados do BigQuery
│   ├── processed/        # Dados limpos e previsões processadas
├── dashboards/
│   └── streamlit_app.py  # Dashboard interativo com Streamlit
├── scripts/
│   ├── bigquery_connector.py # Conexão com BigQuery
│   ├── data_cleaning.py      # Limpeza e preparação dos dados
│   ├── forecasting.py        # Previsões usando Prophet
│   └── ...                   # Outros scripts auxiliares
├── .env                 # Variáveis de ambiente
├── requirements.txt     # Dependências do projeto
├── main.py              # Pipeline principal
└── README.md            # Documentação do projeto
```

## Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas:

- Python 3.8+
- Conta configurada no Google Cloud Platform (GCP)
- Google Cloud SDK

## Configuração

1. **Clonar o Repositório**

   ```sh
   git clone https://github.com/seu-usuario/google-search-trends-analysis.git
   cd google-search-trends-analysis
   ```

2. **Instalar Dependências**

   Certifique-se de que o ambiente virtual está ativado e instale os pacotes listados em `requirements.py`:

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   python requirements.py
   ```

3. **Configurar Variáveis de Ambiente**

   Crie um arquivo `.env` com o seguinte conteúdo:

   ```env
   BIGQUERY_SQL=SELECT refresh_date AS Day, rank AS Rank, score AS Score, region_name AS State, term AS Term FROM `bigquery-public-data.google_trends.international_top_terms` WHERE country_name = "Brazil" AND refresh_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH) AND score IS NOT NULL GROUP BY Day, Rank, Score, State, Term
   LOCATION=US
   ```

4. **Autenticação no Google Cloud**

   Certifique-se de estar autenticado no Google Cloud SDK:

   ```sh
   gcloud auth application-default login
   ```

5. **Executar o Pipeline**

   Para executar a coleta, limpeza e previsão de dados:

   ```sh
   python main.py
   ```

6. **Iniciar o Dashboard**

   Para visualizar o dashboard interativo:

   ```sh
   streamlit run dashboards/streamlit_app.py
   ```

## Funcionalidades

- **Coleta de Dados:** Busca dados do BigQuery utilizando SQL configurado.
- **Limpeza e Preparação:** Remove valores nulos, organiza e agrega dados.
- **Previsões com Prophet:** Gera previsões de tendências de busca por estado e nacionalmente.
- **Dashboard Interativo:** Exibe dados e previsões com gráficos interativos no Streamlit.

## Contato
- Desenvolvedor: [Luís Corrêa](mailto:luisfernandodasilvacorrea@yahoo.com.br)
- GitHub: [LuisFurmiga](https://github.com/LuisFurmiga)
