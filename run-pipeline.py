import os
import subprocess

# Caminho para a pasta onde estão os scripts de scraping
pasta_scraping = "1 - scraping"

# Lista de arquivos Python na ordem desejada
arquivos_scraping = [
    "fpolis_apartamento_aluguel.py",
    "fpolis_apartamento_venda_1quarto.py",
    "fpolis_apartamento_venda_2quartos.py",
    "fpolis_apartamento_venda_3quartos_12banheiros.py",
    "fpolis_apartamento_venda_3quartos_34banheiros.py",
    "fpolis_apartamento_venda_4quartos.py",
    "fpolis_casa_aluguel.py",
    "fpolis_casa_venda_4quartos.py",
    "fpolis_casa_venda_123quartos.py",
    "fpolis_terreno_venda.py",
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
