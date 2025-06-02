"""Database"""
import os
import sys
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis
from config.models import User
from .config import settings

# conexão com MongoDB usando as configurações centralizadas
client = MongoClient(settings.MONGODB_URL)

#  construção dos database que recebe as coleções de dados
db = client.vitivinicultura

# construção de uma coleção que recebe os dados dos usuários do sistema para verificação.
user_collection = db['users']

# construção de uma coleção que recebe os dados do processo de webscrapping.
data_collection = db['data']

# conexão com redis para armazenamento de cache (opcional)
redis = None
try:
    if settings.REDIS_URL and settings.REDIS_URL != "redis://localhost:6379":
        redis = Redis.from_url(settings.REDIS_URL)
        # testa a conexão
        redis.ping()
        print("✅ Redis conectado com sucesso")
    else:
        print("⚠️ Redis não configurado - executando sem cache")
except Exception as e:
    print(f"⚠️ Erro ao conectar Redis: {e} - executando sem cache")
    redis = None

# [AUTH] 30/05/2025 - Função adicionada para suportar autenticação de usuários
async def get_user_by_username(username: str) -> User | None:
    """Busca um usuário pelo username no banco de dados"""
    user_data = user_collection.find_one({"username": username})
    if user_data:
        return User(username=user_data["username"], hashed_password=user_data["hashed_password"])
    return None 