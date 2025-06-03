""" Aplicação Fast API"""
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

sys.path.append('../projeto-api-vitivinicultura')

# Import das rotas existentes (ML)
from routes.route import router
from routes.predict import models_router

# [MERGE] 03/06/2025 - Import da autenticação JWT
from routes.auth import router as auth_router

# [MERGE] 03/06/2025 - Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# construção do objeto app
app = FastAPI(
    title="API de Vitivinicultura com ML e Autenticação",
    version="2.0.0",
    description="API completa para análise, previsão de dados de vitivinicultura e modelos de Machine Learning com autenticação JWT",
    docs_url="/docs",
    redoc_url="/redoc"
)

# [MERGE] 03/06/2025 - Configuração CORS (preservada)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens para facilitar testes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# inclusão das rotas criadas à aplicação.
app.include_router(router, tags=["Dados Vitivinicultura"])
app.include_router(models_router, tags=["Machine Learning"])
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])

logger.info("✅ API completa carregada: Dados + ML + Autenticação JWT")

# [MERGE] 03/06/2025 - Rotas básicas melhoradas
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Bem-vindo à API de Vitivinicultura com ML e Autenticação",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "2.0.0",
        "features": [
            "Dados de Vitivinicultura (1970-2024)",
            "Modelos de Machine Learning",
            "Clustering de países",
            "Previsões de exportação",
            "Autenticação JWT"
        ]
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "api": "online",
            "ml_models": "available", 
            "authentication": "jwt_enabled",
            "data": "connected"
        }
    }
