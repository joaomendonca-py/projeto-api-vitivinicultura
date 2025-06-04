"""App Dashboard Projeto Vitivinicultura"""
from src.train import visualizar_coluna_por_cluster_streamlit
import sys
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import PowerTransformer
sys.path.append('../projeto-api-vitivinicultura')

# atributos da página
st.set_page_config(
    page_title="Dashboard Embrapa",
    page_icon="img/logo_uva.png",
    layout="wide"
)


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("img/fiap.png", width=400)
    st.markdown("""
        <h1 style='text-align: center; color: gray;'>Dados Exportação Vitivinicultura Embrapa</h1>
        <h3 style='text-align: center; color: pink;'>Análise interativa de categorizacao de países</h3>
    """, unsafe_allow_html=True)
    st.markdown("""
        Ese aplicativo foi desenvolvido para ajudar sua análise de perfil dos países compradores de produtos de Vitivinicultura.\n
        Você pode escolher o número de categorias, visualizar os resultados em gráficos interativos 
        e baixar os dados processados com a categoria atribuída.
""")

st.markdown("---")

# definição do número de clusters para conexão
# definição do número de clusters para conexão
n_clusters = st.slider("Selecione o número de categorias:", 2, 11, 2)

# conexão com a api
st.title("Análise de Categorias")

if "data_carregada" not in st.session_state:
    st.session_state.data_carregada = False
    st.session_state.df = None
    st.session_state.X_transformed = None

if st.button("Gerar Visualizações"):
    url = "https://vitivinicultura-00fv.onrender.com/modelo_ML/criar_categorias_clustering"
    payload = {"categorias": n_clusters}
    response = requests.post(url, json=payload)

    if response.status_code == 201:
        try:
            data = response.json()
            if isinstance(data, list):
                df = pd.DataFrame(data)
                if 'categoria' not in df.columns:
                    st.error(
                        "Erro: coluna 'categoria' não está presente nos dados retornados pela API.")
                    st.stop()

                X = df.drop(columns=['pais'])
                transformer = PowerTransformer(
                    method='yeo-johnson', standardize=True)
                output = transformer.fit_transform(
                    X.drop(columns=['categoria']))
                X_transformed = pd.DataFrame(
                    output, columns=[col for col in X.columns if col != 'categoria'])
                X_transformed['categoria'] = df['categoria']

                # Guardar no estado
                st.session_state.df = df
                st.session_state.X_transformed = X_transformed
                st.session_state.data_carregada = True

                st.success("Dados carregados com sucesso!")
            else:
                st.error("Erro: a resposta da API não é uma lista de dicionários.")
        except ValueError:
            st.error("Erro ao decodificar JSON da resposta.")

# Se dados carregados, mostra os gráficos e interatividade
if st.session_state.data_carregada:

    X_transformed = st.session_state.X_transformed
    df = st.session_state.df

    st.subheader("Distribuição dos Países")
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_transformed.drop(columns=['categoria']))

    fig_pca, ax = plt.subplots(figsize=(5, 3))
    sns.scatterplot(
        x=components[:, 0],
        y=components[:, 1],
        hue=X_transformed['categoria'],
        palette='deep',
        ax=ax
    )
    ax.legend(loc='upper right', fontsize=8)
    ax.set_title(
        'Análise da distribuição das categorias por influência de dados.')
    ax.set_xlabel('Influência Indicadores Socioeconômicos', fontsize=7)
    ax.set_ylabel('Influência Indicadores de Transação', fontsize=7)

    st.pyplot(fig_pca)

    st.subheader("Análise dos dados da tabela por categoria")
    coluna_selecionada = st.selectbox(
        "Selecione a coluna para visualizar:",
        options=[col for col in X_transformed.columns if col != 'categoria']
    )

    st.write(f"### Visualização de: {coluna_selecionada}")
    fig = visualizar_coluna_por_cluster_streamlit(
        X_transformed, coluna=coluna_selecionada)
    st.pyplot(fig)

    st.subheader("Tabela de Resultados")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar tabela em CSV",
        data=csv,
        file_name='resultado_clusters.csv',
        mime='text/csv'
    )
