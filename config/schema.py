"""Arquivo gerador de schema de dados do banco de dados"""
from config.models import Processamento, ImportacaoExportacao, ProducaoComercializacao


def obter_item_prod_com_db(data) -> dict:
    """ Função que retorna os dados de produção e comercialização do banco de dados."""
    produto = ProducaoComercializacao(ano=data["ano"],
                            processo=data["processo"],
                            labels=data["labels"],
                            data=data["data"]
                            )
    return produto

def obter_item_processamento_db(data) -> dict:
    """ Função que retorna os dados de processamento do banco de dados."""
    produto = Processamento(ano=data["ano"],
                            processo=data["processo"],
                            tipo_uva=data["tipo_uva"],
                            tipo_uva_texto=data['tipo_uva'],
                            labels=data["labels"],
                            data=data["data"]
                            )
    return produto


def obter_item_import_export_db(data) -> dict:
    """ Função que retorna os dados de importação e exportação do banco de dados."""
    produto = ImportacaoExportacao(
                                    ano=data["ano"],
                                   processo=data["processo"],
                                   produto=data["produto"],
                                   produto_texto=data['produto_texto'],
                                   labels=data["labels"],
                                   data=data["data"]
                                   )
    return produto
