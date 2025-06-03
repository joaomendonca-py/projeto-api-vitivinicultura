"""Database"""
import os
import sys
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis

# constante de conexão com o servidor MongoDB.
URI = os.getenv('DB_URI')
# criação de um cliente para conexão com o servidor.
client = MongoClient(URI)

#  construção dos database que recebe as coleções de dados
db = client.database

# construção de uma coleção que recebe os dados dos usuários do sistema para verificação.
user_collection = db['users']

# construção de uma coleção que recebe os dados do processo de webscrapping.
data_collection = db['data']

# conexão com redis para armazenamento de cache
r_host = os.getenv('REDIS_HOST')
r_port = os.getenv('REDIS_PORT')
r_db = os.getenv('REDIST_DB')

redis = Redis(host=r_host, port=r_port, db=r_port)

# Redis mock para garantir compatibilidade sem erro
class RedisMock:
    def get(self, key):
        return None
    
    def set(self, key, value):
        pass
    
    def expire(self, key, seconds):
        pass

# Importa as configurações do database principal
try:
    from app.database import data_collection
    from app.database import redis as app_redis
    
    # Se redis for None, usa o mock
    redis = app_redis if app_redis is not None else RedisMock()
except:
    redis = RedisMock()
    data_collection = None
