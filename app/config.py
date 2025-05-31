"""Configurações da aplicação"""
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# [AUTH] 30/05/2025 - Configurações adicionadas para JWT e autenticação
# Configurações de autenticação
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_padrao")  # Idealmente, deve ser definida no .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 