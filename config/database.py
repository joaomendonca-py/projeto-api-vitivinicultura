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

redis = Redis(host=r_host, port=r_port, db=r_db)
