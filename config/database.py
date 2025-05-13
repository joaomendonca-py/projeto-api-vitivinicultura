"""Database"""
from pymongo.mongo_client import MongoClient
from redis import Redis

# constante de conexão com o servidor MongoDB.
URI = "mongodb+srv://USER:1234@cluster0.cawsgsm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# criação de um cliente para conexão com o servidor.
client = MongoClient(URI)

#  construção dos database que recebe as coleções de dados
db = client.database

# construção de uma coleção que recebe os dados dos usuários do sistema para verificação.
user_collection = db['users']

# construção de uma coleção que recebe os dados do processo de webscrapping.
data_collection = db['data']

# conexão com redis para armazenamento de cache
redis = Redis(host='localhost', port=6379, db=0)
