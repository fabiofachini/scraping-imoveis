import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import urllib

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

# Criar a conexão com o banco de dados
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(conn_str)

# Nome do arquivo CSV
csv_file = "tabela_transformada.csv"

# Ler o arquivo CSV em um DataFrame
try:
    df = pd.read_csv(csv_file)
    print("Arquivo CSV lido com sucesso.")

    # Inserir os dados no banco de dados
    tabela_destino = "zapimoveis"  # Nome da tabela no banco de dados
    df.to_sql(tabela_destino, engine, if_exists='replace', index=False, schema='imoveis')
    print(f"Dados do arquivo '{csv_file}' salvos com sucesso na tabela '{tabela_destino}' no banco de dados.")
except Exception as e:
    print(f"Erro ao processar o arquivo CSV ou salvar no banco de dados: {e}")

print("Processo concluído.")
