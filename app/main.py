""" Aplicação Fast API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import auth
from .routes.route import router as main_router
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tentar importar rotas de ML
try:
    from .routes.predict import ml_router
    ML_ROUTES_AVAILABLE = True
    logger.info("✅ Rotas de ML encontradas")
except ImportError:
    try:
        from routes.predict import ml_router
        ML_ROUTES_AVAILABLE = True
        logger.info("✅ Rotas de ML encontradas (import alternativo)")
    except ImportError:
        ML_ROUTES_AVAILABLE = False
        logger.info("📋 Rotas de ML não encontradas (opcional)")

# construção do objeto app
app = FastAPI(
    title="API de Vitivinicultura",
    description="API para análise e previsão de dados relacionados à vitivinicultura",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# inclusão das rotas criadas à aplicação.
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(main_router)

# Incluir rotas de ML se disponíveis
if ML_ROUTES_AVAILABLE:
    app.include_router(ml_router)
    logger.info("✅ Rotas de ML incluídas com sucesso")

# Importar outras rotas se existirem
try:
    from .routes import vinhos
    app.include_router(vinhos.router, prefix="/vinhos", tags=["Vinhos"])
    logger.info("✅ Rotas de vinhos carregadas com sucesso")
except ImportError:
    logger.info("📋 Rotas de vinhos não encontradas (opcional)")

try:
    from .routes import predicoes
    app.include_router(predicoes.router, prefix="/predicoes", tags=["Predições"])
    logger.info("✅ Rotas de predições carregadas com sucesso")
except ImportError:
    logger.info("📋 Rotas de predições não encontradas (opcional)")

@app.get("/", tags=["Root"])
@app.head("/", tags=["Root"])  # [DEPLOY] 03/06/2025 - Suporte a health checks HEAD
async def read_root():
    return {
        "message": "Bem-vindo à API de Vitivinicultura",
        "docs": "/docs",
        "redoc": "/redoc",
        "environment": settings.API_ENV,
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health Check"])
@app.head("/health", tags=["Health Check"])  # [DEPLOY] 03/06/2025 - Suporte a health checks HEAD
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.API_ENV,
        "mongodb": "connected" if settings.MONGODB_URL else "not configured",
        "redis": "configured" if settings.REDIS_URL else "not configured"
    }
