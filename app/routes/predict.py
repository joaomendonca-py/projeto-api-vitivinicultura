""""Modularização Rotas API"""
import sys
import pandas as pd
from sklearn.cluster import KMeans
from fastapi import APIRouter
sys.path.append('../projeto-api-vitivinicultura')


# construção do objeto APIRouter.
models_router = APIRouter()


# construção de uma rota post para categorização dos países
@models_router.post("/clustering", status_code=201, 
                    description='Informe o número de categorias que deseja criar para os dados:<br>'  
                    '**Retorno**: tabela com dados de transação e indicadores socioeconômicos dos países.',tags=['modelo_ML'])
async def criar_categorias(categorias: int):
    """Função para gerar categorias de países a partir dos dados de exportação."""
    
    # conversão dos dados em dataframe
    data = pd.read_csv('data/processed/dataset_exportacao_clustering_processed.csv')
    X = data.select_dtypes(include='number')
    kmeans = KMeans(n_clusters=categorias, random_state=42)
    kmeans.fit(X)

    data = data.assign(categoria=kmeans.labels_)
    return data.to_dict(orient='records')
