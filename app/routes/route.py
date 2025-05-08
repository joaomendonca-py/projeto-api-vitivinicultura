""""Modularização Rotas API"""
import json
from fastapi import APIRouter, HTTPException
from config.database import redis # type: ignore
from src.utils import obter_dados_processamento # type: ignore

# construção do objeto APIRouter.
router = APIRouter()


#  construção da rota home
@router.get("/")
async def home():
    """ Função que executa a rota home."""
    return "Bem-vindo(a) a API de dados de Vitivinicultura da Embrapa.\nDados entre 1970 a 2024."


# construção da rota de processamento
@router.get("/processamento", status_code=201)
async def processamento(ano: int):
    """ Função que executa o scrapping dos dados de processamento."""

    # processo try-except: verifica a resposta da página.
    try:
        # pesquisa de dados em cache.
        cache = redis.get(ano)

        if cache:

            print('Dados obtidos por cache')
            return json.loads(cache)

        else:

            # invoca a função para obter os dados da página.
            dados_web = obter_dados_processamento(ano)

            # armazena os dados em cache.
            cache = json.dumps(dados_web)
            redis.set(ano, cache)
            # adiciona o período de tempo de armazenamento.
            redis.expire(ano, 60)
            print('Dados armazenados em cache')
            return dados_web

    # retorna um erro caso a página não estiver disponível.
    except Exception as e:

        return HTTPException(status_code=500, detail=f"Erro: {e}")
