""" Aplicação Fast API"""
from routes.route import router
from fastapi import FastAPI
# from .config.database import user_collection

# construção do objeto app
app = FastAPI(

    title="Dados de Vitivinicultura Embrapa",
    version="1.0.0",
    description="API para captura de dados para uso em modelos de Machine Learning."
)

# inclusão das rotas criadas à aplicação.
app.include_router(router)