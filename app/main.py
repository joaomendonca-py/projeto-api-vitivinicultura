""" Aplicação Fast API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import auth
from .routes.route import router as main_router

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
app.include_router(auth.router, prefix="/auth")
app.include_router(main_router, tags=["Dados Vitivinicultura"])

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Bem-vindo à API de Vitivinicultura",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.API_ENV
    }
