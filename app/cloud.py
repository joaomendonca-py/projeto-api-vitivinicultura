'''Arquivo gerador de backup no banco de dados MongoDB.'''
import sys
sys.path.append('../projeto-api-vitivinicultura')
from src.utils.func_geral import salvar_dados_db

# seleciona a coleção de dados para salvar no banco de dados.
salvar_dados_db('data/collections_importacao2.json', processo='Importação')

# retorno para o usuário
print('Dados salvos com sucesso.')
