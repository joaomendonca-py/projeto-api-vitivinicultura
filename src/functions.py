"""Arquivo de funções gerais"""
import json
from config.database import data_collection  # type: ignore

# função salvar arquivos no formato json.
def salvar_arquivo(output, caminho: str):
    """ Função que gera um backup de dados para uso nas apis."""

    dados = {}
    #conteudo = json.dumps(output, indent=1, sort_keys=True)
    with open(caminho, 'w', encoding='utf-8') as file:
        
        #dados['data'] = output
        conteudo = json.dumps(output, indent=1, sort_keys=True)
        arquivo = file.write(conteudo)

    return arquivo

# função para salvar dados no banco de dados.
def salvar_dados_db(caminho: str):
    """ função que salva os dados no banco de dados """
    with open(caminho, 'r', encoding='utf-8') as file:

        # transforma o arquivo no formato json
        conteudo = json.load(file)
        # insere os arquivos no mongoDB
        for valor in conteudo:
            data_collection.insert_many(valor)

    print('Dados inseridos com sucesso')
