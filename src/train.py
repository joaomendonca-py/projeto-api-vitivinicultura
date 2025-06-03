"""Funções para ajuste de modelo"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.cluster import silhouette_visualizer
from sklearn.cluster import KMeans
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

    fig, ax = plt.subplots(figsize=(6, 4))
    silhouette_visualizer(KMeans(n_clusters=n_cluster), X=df, ax=ax)
    plt.show()   
    plt.close(fig)

def visualizar_coluna_por_cluster(tbl, coluna, cluster_col='cluster'):
    """
    Visualiza um stripplot de uma coluna transformada por cluster, com traço de média.
    
    Parâmetros:
    - tbl: DataFrame com dados transformados e coluna de cluster.
    - coluna: str, nome da coluna para visualizar.
    - cluster_col: str, nome da coluna do cluster, padrão 'cluster'.
    """
    
    plt.figure(figsize=(8, 4))
    
    # Stripplot com valores transformados
    sns.stripplot(
        x=cluster_col, 
        y=coluna, 
        data=tbl, 
        jitter=True, 
        alpha=0.6
    )
    
    # Traço de média por cluster
    mean_values = tbl.groupby(cluster_col)[coluna].mean().reset_index()
    
    sns.pointplot(
        x=cluster_col, 
        y=coluna, 
        data=mean_values, 
        color='red', 
        linestyle='none',       
        err_kws={'linewidth': 0},    
        linewidth=1.5,                
        markersize=6,
        label='Média por cluster'
    )
 
    plt.title(f'Distribuição de {coluna} por Cluster')
    plt.legend()
    plt.ylabel(f'{coluna}')
    plt.xlabel('Cluster')
    plt.show()