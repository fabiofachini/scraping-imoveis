import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import urllib

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do banco de dados
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

# Função para carregar os dados do banco
@st.cache_data
def carregar_dados(tabela="zapimoveis", schema="imoveis"):
    query = f"SELECT * FROM {schema}.{tabela}"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Streamlit UI
st.title("Anúncios de imóveis")

# Carregar os dados
try:
    tabela_destino = "zapimoveis"  # Nome da tabela
    dados = carregar_dados(tabela_destino, schema="imoveis")
    st.success(f"Dados carregados com sucesso da tabela '{tabela_destino}' no schema 'imoveis'.")

    # Seleção de aluguel ou venda
    st.subheader("Selecione o tipo de transação:")
    tipos_transacao = sorted(dados["categoria"].dropna().unique())
    tipo_selecionado = st.selectbox("Aluguel ou Venda:", tipos_transacao)

    # Seleção de tipo de imóvel
    if tipo_selecionado:
        st.subheader("Selecione o tipo de imóvel:")
        tipos_imovel = sorted(
            dados[dados["categoria"] == tipo_selecionado]["tipo"].dropna().unique()
        )
        tipo_imovel_selecionado = st.selectbox("Casa, Apartamento ou Terreno:", tipos_imovel)

        # Seleção de cidades
        if tipo_imovel_selecionado:
            st.subheader("Selecione uma cidade:")
            cidades_disponiveis = sorted(
                dados[
                    (dados["categoria"] == tipo_selecionado) &
                    (dados["tipo"] == tipo_imovel_selecionado)
                ]["cidade"].dropna().unique()
            )
            cidade_selecionada = st.selectbox("Escolha a cidade:", cidades_disponiveis)

            # Seleção de bairros
            if cidade_selecionada:
                st.subheader("Selecione um bairro:")
                bairros_disponiveis = sorted(
                    dados[
                        (dados["categoria"] == tipo_selecionado) &
                        (dados["tipo"] == tipo_imovel_selecionado) &
                        (dados["cidade"] == cidade_selecionada)
                    ]["bairro"].dropna().unique()
                )
                bairro_selecionado = st.selectbox("Escolha o bairro:", bairros_disponiveis)

                # Filtrar dados
                dados_filtrados = dados[
                    (dados["categoria"] == tipo_selecionado) &
                    (dados["tipo"] == tipo_imovel_selecionado) &
                    (dados["cidade"] == cidade_selecionada) &
                    (dados["bairro"] == bairro_selecionado)
                ]

                # Exibir cartões
                st.subheader("Resumo dos dados selecionados")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    st.metric("Nº de anúncios", len(dados_filtrados))
                with col2:
                    st.metric("Mediana - Valor", f"R$ {dados_filtrados['valor'].median():,.2f}")
                with col3:
                    st.metric("Mediana - Metragem", f"{dados_filtrados['metragem'].median():,.2f} m²")
                with col4:
                    st.metric("Mediana - Quartos", int(dados_filtrados["quartos"].median()))
                with col5:
                    st.metric("Mediana - Banheiros", int(dados_filtrados["banheiros"].median()))
                with col6:
                    st.metric("Mediana - Vagas", int(dados_filtrados["vagas"].median()))

                # Exibir tabela filtrada
                st.subheader("Dados Filtrados")
                st.dataframe(dados_filtrados)

                # Botão para exportar para CSV
                st.subheader("Exportar dados para CSV")
                export_button = st.download_button(
                    label="Baixar CSV",
                    data=dados_filtrados.to_csv(index=False),
                    file_name="dados_filtrados.csv",
                    mime="text/csv"
                )

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
