"""Database"""
import os
import sys
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
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

# Redis opcional - se falhar, simplesmente não usa cache
redis = None
print("⚠️ Redis desabilitado - executando sem cache (modo produção)")

# [AUTH] 30/05/2025 - Função adicionada para suportar autenticação de usuários
async def get_user_by_username(username: str) -> User | None:
    """Busca um usuário pelo username no banco de dados"""
    user_data = user_collection.find_one({"username": username})
    if user_data:
        return User(username=user_data["username"], hashed_password=user_data["hashed_password"])
    return None 