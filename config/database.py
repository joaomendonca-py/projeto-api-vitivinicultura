"""Database"""
import os
import sys
import logging
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis

# [DEPLOY] 03/06/2025 - Configurar logging
logger = logging.getLogger(__name__)

# constante de conexão com o servidor MongoDB.
# [DEPLOY] 03/06/2025 - Corrigida variável de ambiente 
URI = os.getenv('MONGODB_URL') or os.getenv('DB_URI')
# criação de um cliente para conexão com o servidor.
client = MongoClient(URI)

#  construção dos database que recebe as coleções de dados
db = client.database

# construção de uma coleção que recebe os dados dos usuários do sistema para verificação.
user_collection = db['users']

# construção de uma coleção que recebe os dados do processo de webscrapping.
data_collection = db['data']

# [DEPLOY] 03/06/2025 - Configuração Redis com fallback para Render
try:
    # Conexão com redis para armazenamento de cache
    r_host = os.getenv('REDIS_HOST', 'localhost')  # Default para desenvolvimento
    r_port = int(os.getenv('REDIS_PORT', '6379'))   # Default Redis port
    r_db = int(os.getenv('REDIS_DB', '0'))          # Corrigido REDIST_DB -> REDIS_DB
    
    redis = Redis(host=r_host, port=r_port, db=r_db, decode_responses=True, socket_connect_timeout=5)
    
    # Testa a conexão
    redis.ping()
    logger.info("✅ Redis conectado com sucesso")
    
except Exception as e:
    logger.warning(f"⚠️ Redis não disponível: {e}")
    logger.info("🔄 Usando cache em memória como fallback")
    
    # Mock Redis para funcionar sem Redis real
    class MockRedis:
        def __init__(self):
            self._cache = {}
            
        def get(self, key):
            return self._cache.get(key)
            
        def set(self, key, value):
            self._cache[key] = value
            return True
            
        def expire(self, key, seconds):
            # Em produção sem Redis, não implementamos TTL
            pass
            
        def ping(self):
            return True
    
    redis = MockRedis()
