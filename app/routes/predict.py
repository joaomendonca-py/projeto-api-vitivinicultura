""""Modularização Rotas API"""
import sys
import json
import pandas as pd
from sklearn.cluster import KMeans
from fastapi import APIRouter, HTTPException
sys.path.append('../projeto-api-vitivinicultura')

# construção do objeto APIRouter.
models_router = APIRouter()

#  construção da rota post para gerar a previsão dos dados
@models_router.post("/predict", tags=['modelos_ML'])
async def previsao_quantidade():
    """ Função que executa a rota home."""
    return 

# construção de uma rota post
@models_router.post("/clustering",tags=['modelos_ML'])
async def criar_categorias(n_cluster: int):

    """Função para gerar categorias de países a partir dos dados de exportação.""" 
    
     # conversão dos dados em dataframe
    data = pd.read_csv('data/processed/dataset_exportacao_clustering_processed.csv')
    X = data.select_dtypes(include='number')
    kmeans = KMeans(n_clusters=n_cluster, random_state=42)
    kmeans.fit(X)

    data = data.assign(cluster=kmeans.labels_)
    return data.to_dict(orient='records')

