""""Modularização Rotas API"""
import sys
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import PowerTransformer
from fastapi import APIRouter
sys.path.append('../projeto-api-vitivinicultura')


# construção do objeto APIRouter.
ml_router = APIRouter()


# construção de uma rota post para categorização dos países
@ml_router.post("/clustering", status_code=201, 
                    description='Informe o número de categorias que deseja criar para os dados:<br>'  
                    '**Retorno**: tabela com dados de transação e indicadores socioeconômicos dos países.',tags=['modelo_ML'])
async def criar_categorias(categorias: int):
    """Função para gerar categorias de países a partir dos dados de exportação."""
    
    # conversão dos dados de entrada em dataframe
    data = pd.read_csv('data/processed/dataset_exportacao_clustering_processed.csv')

    # seleção das colunas numéricas
    X = data.select_dtypes(include='number')

    # scale dos dados
    transformer = PowerTransformer(method='yeo-johnson', standardize=True)
    output = transformer.fit_transform(X)

    # construção de um dataset transformado
    X_transformed = pd.DataFrame(
        output,
        columns=X.columns,
        index=X.index
    )
    
    # instância do modelo com o parâmetro do usuário
    kmeans = KMeans(n_clusters=categorias, random_state=42)

    # ajuste do modelo
    kmeans.fit(X_transformed)

    # inserção do label do modelo ao dataset
    data = data.assign(categoria=kmeans.labels_)
    return data.to_dict(orient='records')
