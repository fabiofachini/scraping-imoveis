import streamlit as st
import pandas as pd
import pymssql
import os
from dotenv import load_dotenv

# Configurar a página para modo wide
st.set_page_config(page_title="Anúncios de imóveis", layout="wide")

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do banco de dados
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

# Função para carregar os dados do banco
@st.cache_data
def carregar_dados(tabela="zapimoveis", schema="imoveis"):
    try:
        with pymssql.connect(server, username, password, database) as conn:
            query = f"SELECT * FROM {schema}.{tabela}"
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Streamlit UI
st.title("Anúncios de imóveis")

# Carregar os dados
try:
    tabela_destino = "zapimoveis"  # Nome da tabela
    dados = carregar_dados(tabela_destino, schema="imoveis")
    if not dados.empty:
        st.success(f"Dados carregados com sucesso.")

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

                    # Exibir métricas
                    st.subheader("Resumo dos dados selecionados")
                    st.metric("Nº de anúncios", len(dados_filtrados))
                    st.dataframe(dados_filtrados)

                    # Botão para exportar para CSV
                    st.subheader("Exportar dados para CSV")
                    st.download_button(
                        label="Baixar CSV",
                        data=dados_filtrados.to_csv(index=False),
                        file_name="dados_filtrados.csv",
                        mime="text/csv"
                    )
    else:
        st.warning("Nenhum dado encontrado!")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
