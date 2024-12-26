import pandas as pd
import os

# Lista de arquivos CSV
arquivos_scraping = [
    "fpolis_aluguel_apartamento_tudo.csv",
    "fpolis_venda_apartamento_1quarto.csv",
    "fpolis_venda_apartamento_2quartos.csv",
    "fpolis_venda_apartamento_3quartos_12banheiros.csv",
    "fpolis_venda_apartamento_3quartos_34banheiros.csv",
    "fpolis_venda_apartamento_4quartos.csv",
    "fpolis_aluguel_casa_tudo.csv",
    "fpolis_venda_casa_4quartos.csv",
    "fpolis_venda_casa_123quartos.csv",
    "fpolis_venda_terreno_tudo.csv",
]

# Caminho da pasta com os arquivos CSV
pasta_csv = "2 - csv"

# Leitura e combinação dos arquivos em um único DataFrame
dataframes = []
for arquivo in arquivos_scraping:
    caminho_arquivo = os.path.join(pasta_csv, arquivo)
    if os.path.exists(caminho_arquivo):  # Verificar se o arquivo existe
        df_temp = pd.read_csv(caminho_arquivo)
        dataframes.append(df_temp)
    else:
        print(f"Arquivo não encontrado: {caminho_arquivo}")

# Concatenar os DataFrames
df = pd.concat(dataframes, ignore_index=True)

# Separar a coluna "titulo" em "bairro" e "cidade"
df[['bairro', 'cidade']] = df['titulo'].str.split(', ', expand=True)

# Extrair "dia/mes" da coluna "valor" antes da conversão
df['dia/mes'] = df['valor'].str.extract(r'\/(.*)')

# Processar a coluna "valor" para lidar com o padrão brasileiro
df['valor'] = df['valor'].str.replace('.', '', regex=False)  # Remover separadores de milhar
df['valor'] = df['valor'].str.replace(',', '.', regex=False)  # Substituir vírgula por ponto
df['valor'] = df['valor'].str.extract(r'(\d+\.?\d*)').astype(float)  # Converter para float

# Remover o "m²" da coluna `metragem`
df['metragem'] = df['metragem'].str.replace(' m²', '', regex=False)

# Extrair o maior valor de colunas com valores separados por traço
for coluna in ['metragem', 'quartos', 'banheiros', 'vagas']:
    df[coluna] = df[coluna].astype(str).str.split('-').apply(
        lambda x: max([float(i) for i in x]) if isinstance(x, list) else float(x)
    )

# Processar e converter tipos de colunas
df['vagas'] = df['vagas'].fillna(0).astype(float).astype(int)
df['valor'] = df['valor'].fillna(0).astype(int)
df['metragem'] = df['metragem'].fillna(0).astype(int)
df['quartos'] = df['quartos'].fillna(0).astype(int)
df['banheiros'] = df['banheiros'].fillna(0).astype(int)

# Remover duplicatas
df = df.drop_duplicates(subset=[
    'categoria', 'tipo', 'bairro', 'cidade', 'endereco', 'valor', 
    'dia/mes', 'metragem', 'quartos', 'banheiros', 'vagas', 'link'
])

# Preencher valores ausentes ou em branco na coluna "link"
df['link'] = df['link'].fillna("Vários anúncios para o mesmo imóvel")
df['link'] = df['link'].replace(r'^\s*$', "Vários anúncios para o mesmo imóvel", regex=True)

# Reorganizar colunas
colunas_final = [
    'categoria', 'tipo', 'bairro', 'cidade', 'endereco', 'valor', 'dia/mes',
    'metragem', 'quartos', 'banheiros', 'vagas', 'link', 'timestamp'
]
df = df[colunas_final]

# Salvar o DataFrame transformado em um novo CSV
df.to_csv("tabela_transformada.csv", index=False)

# Mostrar o DataFrame resultante
print(df)
