"""Database"""
import os
import sys
import logging
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis
from config.models import User

# [DEPLOY] 03/06/2025 - Configurar logging
logger = logging.getLogger(__name__)

# [DEPLOY] 03/06/2025 - Corrigir conexão MongoDB Atlas
# Usar MONGODB_URL em vez de DB_URI para consistência com config.py
URI = os.getenv('MONGODB_URL', 'mongodb+srv://projeto5mlet:projetofiap@apiembrapa.wcmp3fv.mongodb.net/?retryWrites=true&w=majority&appName=apiEmbrapa')

# criação de um cliente para conexão com o servidor.
client = MongoClient(URI)

#  construção dos database que recebe as coleções de dados
db = client.vitivinicultura

# construção de uma coleção que recebe os dados dos usuários do sistema para verificação.
user_collection = db['users']

# construção de uma coleção que recebe os dados do processo de webscrapping.
data_collection = db['data']

# [DEPLOY] 03/06/2025 - Configuração Redis com fallback para Render
try:
    r_host = os.getenv('REDIS_HOST', 'localhost')
    r_port = int(os.getenv('REDIS_PORT', 6379))
    r_db = int(os.getenv('REDIS_DB', 0))

    redis = Redis(host=r_host, port=r_port, db=r_db, decode_responses=True, socket_connect_timeout=5)
    
    # Testa a conexão
    redis.ping()
    logger.info("✅ Redis conectado com sucesso no app/database.py")
    
except Exception as e:
    logger.warning(f"⚠️ Redis não disponível no app/database.py: {e}")
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

# [AUTH] 30/05/2025 - Função adicionada para suportar autenticação de usuários
async def get_user_by_username(username: str) -> User | None:
    """Busca um usuário pelo username no banco de dados"""
    try:
        user_data = user_collection.find_one({"username": username})
        if user_data:
            return User(username=user_data["username"], hashed_password=user_data["hashed_password"])
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar usuário: {e}")
        return None 