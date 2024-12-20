import pandas as pd
import os

# Caminho da pasta com os arquivos CSV
pasta_csv = "2 - csv"

# Leitura dos arquivos na pasta
arquivo1 = os.path.join(pasta_csv, "aluguel_apartamento_florianopolis.csv")
arquivo2 = os.path.join(pasta_csv, "venda_apartamento_florianopolis.csv")

# Leitura dos dois DataFrames
df1 = pd.read_csv(arquivo1)
df2 = pd.read_csv(arquivo2)

# Combinar as duas tabelas
df = pd.concat([df1, df2], ignore_index=True)

# Separar a coluna "titulo" em "bairro" e "cidade"
df[['bairro', 'cidade']] = df['titulo'].str.split(', ', expand=True)

# Extrair "dia/mes" da coluna "valor" antes da conversão
df['dia/mes'] = df['valor'].str.extract(r'\/(.*)')

# Processar a coluna "valor" para lidar com o padrão brasileiro
df['valor'] = df['valor'].str.replace('.', '', regex=False)  # Remover separadores de milhar
df['valor'] = df['valor'].str.replace(',', '.', regex=False)  # Substituir vírgula por ponto
df['valor'] = df['valor'].str.extract(r'(\d+\.?\d*)').astype(float)  # Converter para float

# 1. Remover o "m²" da coluna `metragem`
df['metragem'] = df['metragem'].str.replace(' m²', '', regex=False)

# 2. Extrair o maior valor de colunas com valores separados por traço
for coluna in ['metragem', 'quartos', 'banheiros', 'vagas']:
    # Garantir que a coluna tenha valores como strings
    df[coluna] = df[coluna].astype(str)  # Convertendo para string
    df[coluna] = df[coluna].str.split('-').apply(lambda x: max([float(i) for i in x]) if isinstance(x, list) else float(x))

# 3. Remover o ponto na coluna `vagas` (convertendo para inteiro)
df['vagas'] = df['vagas'].fillna(0)
df['vagas'] = df['vagas'].astype(float).astype(int)  # Primeiro converte para float, depois para int
df['valor'] = df['valor'].astype(int)
df['metragem'] = df['metragem'].astype(int)
df['quartos'] = df['quartos'].astype(int)
df['banheiros'] = df['banheiros'].astype(int)

# Remover duplicatas (linhas que são exatamente iguais em todas as colunas)
df = df.drop_duplicates()

df = df[['categoria', 'tipo', 'bairro', 'cidade', 'endereco', 'valor', 'dia/mes', 'metragem', 'quartos', 'banheiros', 'vagas', 'link','timestamp']]

# Salvar o DataFrame transformado em um novo CSV
df.to_csv("tabela_transformada.csv", index=False)

# Mostrar o DataFrame resultante
print(df)
