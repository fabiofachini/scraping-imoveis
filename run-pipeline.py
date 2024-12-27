import os
import subprocess

# Caminhos para as pastas
pasta_scraping = "1 - scraping"
pasta_transformacao = "3 - transformacao"
pasta_transferencia = "4 - transferencia"

# Lista de arquivos Python para scraping, na ordem desejada
arquivos_scraping = [
    "fpolis_aluguel_apartamento.py",
    "fpolis_aluguel_casa.py",
    "fpolis_venda_apartamento_1quarto.py",
    "fpolis_venda_apartamento_2quartos_2banheiros.py",
    "fpolis_venda_apartamento_2quartos_134banheiros.py",
    "fpolis_venda_apartamento_3quartos_12banheiros.py",
    "fpolis_venda_apartamento_3quartos_34banheiros.py",
    "fpolis_venda_apartamento_4quartos.py",
    "fpolis_venda_casa_3quartos.py",
    "fpolis_venda_casa_4quartos.py",
    "fpolis_venda_casa_12quartos.py",
    "fpolis_venda_terreno.py",
]

# Executar os scripts de scraping
for arquivo in arquivos_scraping:
    print(f"Executando {arquivo}...")
    subprocess.run(["python", os.path.join(pasta_scraping, arquivo)])

# Executar o script de transformação
print("Executando transformacao.py...")
subprocess.run(["python", os.path.join(pasta_transformacao, "transformacao.py")])

# Executar o script de transferência
print("Executando transferencia.py...")
subprocess.run(["python", os.path.join(pasta_transferencia, "transferencia.py")])
