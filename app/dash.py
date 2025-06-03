"""App Dashboard Projeto Vitivinicultura"""
import sys
import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import PowerTransformer
from PIL import Image
sys.path.append('../projeto-api-vitivinicultura')
from src.train import visualizar_coluna_por_cluster

# -------------------- Configurações da Página --------------------
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
                Teste
    """, unsafe_allow_html=True)
    st.markdown("""
        Ese aplicativo foi desenvolvido para ajudar sua análise de perfil de países importadores.<br>
        Você pode escolher o número de categorias, visualizar os resultados em gráficos interativos 
        e baixar os dados processados.
""")

st.markdown("---")

# -------------------- Parâmetro de Clusters --------------------
n_clusters = st.slider("Selecione o número de clusters:", 2, 11, 1)

# -------------------- Consumo da API --------------------
st.write("Consultando a API...")

# Simulação de chamada à API que retorna um dataframe com cluster
# Exemplo: response = requests.post('https://suaapi/model', json={'n_clusters': n_clusters})
# df = pd.DataFrame(response.json())

# --- Para teste local: cria um dataset de exemplo ---
np.random.seed(42)
X = np.random.randn(150, 4)

# scale dos dados
transformer = PowerTransformer(method='yeo-johnson', standardize=True)
output = transformer.fit_transform(X)

df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4'])
df['cluster'] = np.random.choice(range(n_clusters), size=len(df))

# -------------------- Gráfico PCA --------------------
st.subheader("Distribuição via PCA")

pca = PCA(n_components=2)
components = pca.fit_transform(df.drop(['pais','cluster'], axis=1))

fig_pca, ax = plt.subplots()
sns.scatterplot(
    x=components[:, 0],
    y=components[:, 1],
    hue=df['cluster'],
    palette='deep',
    ax=ax
)
ax.set_title('Análise da distribuição dos clusters')
ax.set_xlabel('Influência Indicadores Socio-econômicos')
ax.set_ylabel('Influência Indicadores de Transação')

st.pyplot(fig_pca)

# -------------------- Gráfico Stripplot --------------------
st.subheader("Distribuição de uma variável por cluster")

# Seleção da coluna
st.sidebar.header("Configurações")
coluna_selecionada = st.sidebar.selectbox(
    "Selecione a coluna para visualizar:",
    options=[col for col in tbl.columns if col != 'cluster']
)

st.write(f"### Visualização de: {coluna_selecionada}")

# Gerando o gráfico com a função que você criou
fig = plt.figure(figsize=(8, 4))
visualizar_coluna_por_cluster(tbl, coluna=coluna_selecionada)
st.pyplot(fig)

# -------------------- Tabela de Resultados --------------------
st.subheader("Tabela de Resultados")

st.dataframe(df)

# -------------------- Download da Tabela --------------------
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Baixar tabela em CSV",
    data=csv,
    file_name='resultado_clusters.csv',
    mime='text/csv'
)
