"""Modelo de Dados"""
from typing import List
from pydantic import BaseModel

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
