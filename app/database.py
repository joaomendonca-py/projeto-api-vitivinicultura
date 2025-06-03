"""Database"""
import os
import sys
sys.path.append('../projeto-api-vitivinicultura')
from pymongo.mongo_client import MongoClient
from redis import Redis
from config.models import User
import logging

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

# [HOTFIX] 03/06/2025 - Configuração Redis Cloud com autenticação
def setup_redis():
    """Configura Redis Cloud com tratamento de erro para ambiente de produção"""
    try:
        # Verifica se a URL completa do Redis está disponível
        redis_url = os.getenv('REDIS_URL')
        if redis_url:
            # Usa a URL completa do Redis Cloud
            redis_client = Redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=10)
            logging.info(f"✅ Tentando conectar Redis Cloud: {redis_url.split('@')[1] if '@' in redis_url else redis_url}")
        else:
            # Fallback para configuração manual
            r_host = os.getenv('REDIS_HOST', 'localhost')
            r_port = os.getenv('REDIS_PORT', '6379')
            r_password = os.getenv('REDIS_PASSWORD')
            r_username = os.getenv('REDIS_USERNAME', 'default')
            r_db = os.getenv('REDIS_DB', '0')
            
            # Converte para int com tratamento de erro
            if r_port and r_port.strip():
                r_port = int(r_port)
            else:
                r_port = 6379
                
            if r_db and r_db.strip():
                r_db = int(r_db)
            else:
                r_db = 0
            
            # Cria conexão Redis com autenticação
            redis_client = Redis(
                host=r_host, 
                port=r_port, 
                db=r_db, 
                password=r_password,
                username=r_username,
                decode_responses=True, 
                socket_connect_timeout=10
            )
            logging.info(f"✅ Tentando conectar Redis: {r_host}:{r_port}")
        
        # Testa a conexão
        redis_client.ping()
        logging.info("✅ Redis conectado com sucesso!")
        return redis_client
        
    except Exception as e:
        logging.warning(f"⚠️ Redis não disponível: {e}. Funcionando sem cache.")
        return None

# Inicializa Redis
redis = setup_redis()

class MockRedis:
    """Mock do Redis para quando não estiver disponível"""
    def get(self, key):
        return None
    
    def set(self, key, value):
        return True
    
    def expire(self, key, seconds):
        return True

# Se Redis não estiver disponível, usa mock
if redis is None:
    redis = MockRedis()
    logging.info("🔄 Usando MockRedis - cache desabilitado")

# [AUTH] 30/05/2025 - Função adicionada para suportar autenticação de usuários
async def get_user_by_username(username: str) -> User | None:
    """Busca um usuário pelo username no banco de dados"""
    try:
        user_data = user_collection.find_one({"username": username})
        if user_data:
            return User(username=user_data["username"], hashed_password=user_data["hashed_password"])
        return None
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None 