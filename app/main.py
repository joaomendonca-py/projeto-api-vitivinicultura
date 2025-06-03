""" Aplicação Fast API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# [DEPLOY] 03/06/2025 - Configurar logging
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

logger.info("✅ API básica carregada - teste de deploy")

# [DEPLOY] 03/06/2025 - Rotas básicas para teste
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Bem-vindo à API de Vitivinicultura com ML e Autenticação",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "2.0.0",
        "status": "deploy_test",
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
        "deploy": "test_mode",
        "services": {
            "api": "online",
            "ml_models": "loading", 
            "authentication": "loading",
            "data": "loading"
        }
    }

# [DEPLOY] 03/06/2025 - Teste básico de importação
try:
    # Import das rotas existentes (ML) - teste gradual
    from app.routes.route import router
    app.include_router(router, tags=["Dados Vitivinicultura"])
    logger.info("✅ Rotas de dados carregadas")
except ImportError as e:
    logger.warning(f"⚠️ Rotas de dados não carregadas: {e}")

try:
    from app.routes.predict import models_router
    app.include_router(models_router, tags=["Machine Learning"])
    logger.info("✅ Rotas ML carregadas")
except ImportError as e:
    logger.warning(f"⚠️ Rotas ML não carregadas: {e}")

try:
    # [MERGE] 03/06/2025 - Import da autenticação JWT - teste
    from app.routes.auth import router as auth_router
    app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
    logger.info("✅ Rotas de autenticação carregadas")
except ImportError as e:
    logger.warning(f"⚠️ Rotas de autenticação não carregadas: {e}")

logger.info("🚀 API inicializada - verificar logs para status dos módulos")
