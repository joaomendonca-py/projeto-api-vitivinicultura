"""Rotas de autenticação"""
# [AUTH] 30/05/2025 - Módulo criado para implementar autenticação JWT com FastAPI
from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, validator
import re
import sys

# [MERGE] 03/06/2025 - Ajustar imports para nova estrutura
sys.path.append('../projeto-api-vitivinicultura')

# Imports locais ajustados
try:
    from config import settings
except ImportError:
    # Fallback para configurações básicas
    class Settings:
        JWT_SECRET_KEY = "fallback-secret-key-change-in-production"
        JWT_ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 30
    settings = Settings()

try:
    from database import get_user_by_username, user_collection
except ImportError:
    try:
        from app.database import get_user_by_username, user_collection
    except ImportError:
        # Mock para teste sem banco
        async def get_user_by_username(username):
            return None
        user_collection = None

try:
    from config.models import User
except ImportError:
    # Modelo básico de User
    class User:
        def __init__(self, username, hashed_password):
            self.username = username
            self.hashed_password = hashed_password

router = APIRouter()

# Configuração do contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# [AUTH] 30/05/2025 - Modelos Pydantic para autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário (3-50 caracteres)")
    password: str = Field(..., min_length=6, description="Senha com pelo menos 6 caracteres, incluindo letras e números")
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username deve conter apenas letras, números, _ ou -')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        
        # Verifica se tem pelo menos uma letra
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra')
        
        # Verifica se tem pelo menos um número
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        
        return v

class UserResponse(BaseModel):
    username: str
    message: str

# [AUTH] 30/05/2025 - Funções de gerenciamento de tokens JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

# [DEPLOY] 03/06/2025 - Rota de login melhorada para compatibilidade com Swagger
@router.post("/token", response_model=Token, summary="Login - Obter Token JWT")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: Optional[str] = Form(default="password"),
    scope: str = Form(default=""),
    client_id: Optional[str] = Form(default=None),
    client_secret: Optional[str] = Form(default=None)
):
    """
    Faz login e retorna um token JWT.
    
    Envie username e password via form-data.
    O token retornado deve ser usado no header: Authorization: Bearer {token}
    """
    user = await get_user_by_username(username.lower())
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# [DEPLOY] 03/06/2025 - Endpoint adicional de login usando JSON para testes diretos
@router.post("/login", response_model=Token, summary="Login Alternativo - JSON")
async def login_json(request: TokenRequest):
    """
    Login alternativo usando JSON (para testes com curl/Postman)
    """
    user = await get_user_by_username(request.username.lower())
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# [AUTH] 30/05/2025 - Rota de registro de novos usuários
@router.post("/signup", response_model=UserResponse, summary="Cadastro - Criar Nova Conta")
async def create_user(user: UserCreate):
    """
    Cria uma nova conta de usuário.
    
    Regras:
    - Username: 3-50 caracteres, apenas letras, números, _ ou -
    - Senha: mínimo 6 caracteres, deve conter pelo menos 1 letra e 1 número
    """
    if not user_collection:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados não disponível"
        )
    
    # Verifica se o usuário já existe
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso"
        )
    
    # Cria o hash da senha
    hashed_password = pwd_context.hash(user.password)
    
    # Cria o usuário no banco
    user_dict = {
        "username": user.username,
        "hashed_password": hashed_password
    }
    user_collection.insert_one(user_dict)
    
    return {
        "username": user.username,
        "message": "Usuário criado com sucesso! Use /auth/token para fazer login."
    }

# Rota protegida para testar autenticação
@router.get("/me", response_model=dict, summary="Perfil - Dados do Usuário Logado")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retorna informações do usuário autenticado.
    
    Requer token JWT no header: Authorization: Bearer {token}
    """
    return {
        "username": current_user.username,
        "message": "Usuário autenticado com sucesso!"
    }
