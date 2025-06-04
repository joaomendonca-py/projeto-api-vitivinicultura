"""Database"""
import os
import sys
<<<<<<< HEAD
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis
=======
import logging
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient

# Configurar logging
logger = logging.getLogger(__name__)
>>>>>>> ee91b8155e98a8084edee1553139a2c0fe5c814e

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

<<<<<<< HEAD
# conexão com redis para armazenamento de cache
r_host = os.getenv('REDIS_HOST')
r_port = os.getenv('REDIS_PORT')
r_db = os.getenv('REDIST_DB')

redis = Redis(host=r_host, port=r_port, db=r_db)
=======
# conexão com redis para armazenamento de cache com fallback
try:
    from redis import Redis
    
    # Corrigir erro de digitação: REDIST_DB -> REDIS_DB
    r_host = os.getenv('REDIS_HOST', 'localhost')
    r_port = os.getenv('REDIS_PORT', 6379)
    r_db = os.getenv('REDIS_DB', 0)
    
    # Verificar se temos configurações válidas
    if r_host and r_port:
        redis = Redis(host=r_host, port=int(r_port), db=int(r_db))
        # Testar conexão
        redis.ping()
        logger.info("✅ Redis conectado com sucesso")
    else:
        raise Exception("Configurações Redis não disponíveis")
        
except Exception as e:
    logger.warning(f"⚠️ Redis não disponível: {e}. Usando MockRedis.")
    
    # Implementar MockRedis simples
    class MockRedis:
        def __init__(self):
            self.data = {}
            
        def get(self, key):
            return None  # Always return None (no cache)
            
        def set(self, key, value):
            return True  # Simulate success
            
        def expire(self, key, seconds):
            return True  # Simulate success
            
        def ping(self):
            return True
    
    redis = MockRedis()
    logger.info("✅ MockRedis ativo - funcionando sem cache")
>>>>>>> ee91b8155e98a8084edee1553139a2c0fe5c814e
