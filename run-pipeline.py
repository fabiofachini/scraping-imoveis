import os
import subprocess

# Caminho para a pasta onde estão os scripts de scraping
pasta_scraping = "1 - scraping"

# Lista de arquivos Python na ordem desejada
arquivos_scraping = [
    "fpolis_aluguel_apartamento.py",
    "fpolis_aluguel_casa.py",
    "fpolis_venda_apartamento_1quarto.py",
    "fpolis_venda_apartamento_2quartos.py",
    "fpolis_venda_apartamento_3quartos_12banheiros.py",
    "fpolis_venda_apartamento_3quartos_34banheiros.py",
    "fpolis_venda_apartamento_4quartos.py",
    "fpolis_venda_casa_4quartos.py",
    "fpolis_venda_casa_123quartos.py",
    "fpolis_venda_terreno.py",
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
