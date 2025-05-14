"""Arquivo gerador de schema de dados do banco de dados"""
from config.models import Processamento
def obter_item_processamento_db(data) -> dict:
    """ Função que retorna os dados do banco de dados."""   
    produto = Processamento(ano = data["ano"],
                            processo = data["processo"],
                            tipo_uva = data["tipo_uva"],
                            tipo_uva_texto= data['tipo_uva'],
                            labels = data["labels"],
                            data = data["data"]
                            )
    return produto
