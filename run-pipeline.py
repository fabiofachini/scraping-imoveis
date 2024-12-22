import os
import subprocess

# Caminho para a pasta onde estão os scripts de scraping
pasta_scraping = "1 - scraping"

# Lista de arquivos Python na ordem desejada
arquivos_scraping = [
    "apartamento_aluguel_florianopolis.py",
    "apartamento_venda_florianopolis.py",
    "casa_aluguel_florianopolis.py",
    "casa_venda_florianopolis.py",
    "terreno_venda_florianopolis.py",
]

# Função para executar os scripts de scraping
for arquivo in arquivos_scraping:
    caminho_arquivo = os.path.join(pasta_scraping, arquivo)
    if os.path.exists(caminho_arquivo):
        print(f"Executando {arquivo}...")
        try:
            subprocess.run(["python", caminho_arquivo], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar {arquivo}: {e}")
    else:
        print(f"Arquivo {arquivo} não encontrado na pasta {pasta_scraping}.")

# Caminho para o arquivo de transformação
pasta_transformacao = "3 - transformacao"
arquivo_transformacao = "transformacao.py"
caminho_transformacao = os.path.join(pasta_transformacao, arquivo_transformacao)

# Executar o script de transformação
if os.path.exists(caminho_transformacao):
    print(f"Executando {arquivo_transformacao}...")
    try:
        subprocess.run(["python", caminho_transformacao], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {arquivo_transformacao}: {e}")
else:
    print(f"Arquivo {arquivo_transformacao} não encontrado na pasta {pasta_transformacao}.")
