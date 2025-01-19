# bigquery_connector.py
from google.cloud import bigquery

def fetch_data(query, location):
    client = bigquery.Client(location=location)  # Região do dataset público
    return client.query(query).to_dataframe()
