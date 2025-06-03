"""Modelo de Dados"""
from typing import List
from pydantic import BaseModel


class Processamento(BaseModel):
    """Classe que recebe os dados de Processamento."""
    ano: int
    processo: str
    tipo_uva: str
    tipo_uva_texto: str
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

    def expand_data(self):
        """ Função que retorna os dados de forma de lista para transformação tabular."""
        linhas = []
        for linha in self.data:
            linha_dict = {
                'ano': self.ano,
                'processo': self.processo,
                'produto': self.produto,
                'produto_texto': self.produto_texto,
                self.labels[0]: linha[0],
                self.labels[1]: linha[1],
                self.labels[2]: linha[2],
            }
            linhas.append(linha_dict)
        return linhas
