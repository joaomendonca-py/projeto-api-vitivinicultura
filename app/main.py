""" Aplicação Fast API"""
from fastapi import FastAPI
from app.routes.route import router
from app.routes import auth

# construção do objeto app
app = FastAPI(
    title="Dados de Vitivinicultura Embrapa",
    version="1.0.0",
    description="API para captura de dados para uso em modelos de Machine Learning."
)

# inclusão das rotas criadas à aplicação.
app.include_router(router)
# adiciona o router de autenticação
app.include_router(auth.router)
