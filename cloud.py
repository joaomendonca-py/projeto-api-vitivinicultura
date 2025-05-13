'''Arquivo gerador de backup no banco de dados MongoDB.'''
from src.utils import salvar_dados_db

# seleciona a coleção de dados para salvar no banco de dados.
salvar_dados_db('./data/collections_processamento.json')

# retorno para o usuário
print('Dados salvos com sucesso.')
