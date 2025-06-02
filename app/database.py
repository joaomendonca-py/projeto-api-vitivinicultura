"""Database"""
import os
import sys
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis
from config.models import User

# constante de conexão com o servidor MongoDB.
URI = os.getenv('DB_URI', 'mongodb://admin:admin@localhost:27017/vitivinicultura?authSource=admin')
# criação de um cliente para conexão com o servidor.
client = MongoClient(URI)

#  construção dos database que recebe as coleções de dados
db = client.vitivinicultura

# construção de uma coleção que recebe os dados dos usuários do sistema para verificação.
user_collection = db['users']

# construção de uma coleção que recebe os dados do processo de webscrapping.
data_collection = db['data']

# conexão com redis para armazenamento de cache
r_host = os.getenv('REDIS_HOST', 'localhost')
r_port = os.getenv('REDIS_PORT', 6379)
r_db = os.getenv('REDIS_DB', 0)

redis = Redis(host=r_host, port=r_port, db=r_db)

# [AUTH] 30/05/2025 - Função adicionada para suportar autenticação de usuários
async def get_user_by_username(username: str) -> User | None:
    """Busca um usuário pelo username no banco de dados"""
    user_data = user_collection.find_one({"username": username})
    if user_data:
        return User(username=user_data["username"], hashed_password=user_data["hashed_password"])
    return None 