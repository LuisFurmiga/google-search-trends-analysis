import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = [
    "pandas",
    "numpy",
    "matplotlib",
    "streamlit",
    "python-dotenv",
    "google-cloud-bigquery",
    "google-cloud-storage",
    "google-cloud-bigquery-storage",
    "cmdstanpy",
    "prophet"
]

# Instalar pacotes Python
for package in required_packages:
    install(package)

print("Todos os pacotes necessários foram instalados com sucesso!")
