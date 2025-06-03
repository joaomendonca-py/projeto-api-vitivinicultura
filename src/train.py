"""Funções para ajuste de modelo"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.cluster import silhouette_visualizer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PowerTransformer
def montar_formula(target, features):
    """
    Monta uma fórmula para smf.ols usando Q() para proteger variáveis com nomes complexos.
    
    target : str → nome da variável alvo
    features : list → lista de nomes das features
    """
    target_q = f"Q('{target}')"
    features_q = " + ".join([f"Q('{feat}')" for feat in features])
    formula = f"{target_q} ~ {features_q}"
    return formula


def analise_silhouette(n_cluster, df=pd.DataFrame):
    """Função que retorna a análise gráfica Silhouette"""
    silhouette_visualizer(KMeans(n_clusters=n_cluster), X=df)
    return plt.show()

def visualizar_coluna_por_cluster(tbl, coluna, cluster_col='cluster'):
    """
    Visualiza um stripplot de uma coluna por cluster, revertendo a transformação de escala
    com traço de média.
    
    Parâmetros:
    - tbl: DataFrame com dados transformados e coluna de cluster.
    - coluna: str, nome da coluna para visualizar.
    - cluster_col: str, nome da coluna do cluster, padrão 'cluster'.
    """
    
    df_plot = tbl.copy()
    
    # Reverter a transformação para a coluna selecionada
    col_index = list(df_plot.columns).index(coluna)
    
    # Mantém a coluna do cluster para plotar depois
    cluster_data = df_plot[cluster_col]
    
    # Remove colunas não numéricas para o PowerTransformer
    df_plot = df_plot.select_dtypes(include=[np.number])
    
    # Ajusta PowerTransformer
    pt = PowerTransformer(method='yeo-johnson')
    pt.fit(df_plot)
    
    # Reverte a transformação de toda a matriz
    dados_invertidos = pt.inverse_transform(df_plot)
    
    # Substitui a coluna transformada pela revertida
    df_plot[coluna + '_original'] = dados_invertidos[:, col_index]
    
    # Adiciona de volta a coluna do cluster
    df_plot[cluster_col] = cluster_data.values
    
    plt.figure(figsize=(8, 4))
    
    # Stripplot com valores revertidos
    sns.stripplot(x=cluster_col, y=coluna + '_original', data=df_plot, jitter=True, alpha=0.6)
    
    # Traço de média por cluster
    mean_values = df_plot.groupby(cluster_col)[coluna + '_original'].mean().reset_index()
    
    sns.pointplot(x=cluster_col, y=coluna + '_original', data=mean_values, 
                  color='red', scale=1.5, join=False, errwidth=0)
    
    plt.title(f'Distribuição de {coluna} (escala original) por Cluster')
    plt.ylabel(f'{coluna} (escala original)')
    plt.xlabel('Cluster')
    plt.show()

