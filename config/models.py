"""Modelo de Dados"""
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext

class Processamento(BaseModel):
    """Classe que recebe os dados de Processamento."""
    ano: int
    processo: str
    tipo_uva: str
    tipo_uva_texto:str
    labels: List[str]
    data: List[list]

class ProducaoComercializacao(BaseModel):
    """Classe que recebe os dados de Produção e Comercialização."""
    ano: int
    processo: str
    labels: List[str]
    data: List[List]

class ImportacaoExportacao(BaseModel):
    """Classe que recebe os dados de Importação e Exportação."""
    ano: int
    processo: str
    produto: str
    produto_texto: str
    labels: List[str]
    data: List[List]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)