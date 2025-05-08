"""Arquivo gerador de backup dos dados com webscrapping."""
from src.utils import obter_dados_processamento
from src.functions import salvar_arquivo  # type: ignore

# início do processo
print('Em execução. Capturando dados.')
# objeto que armazena os dados da pesquisa.
lista = []

# laço de repetição para armazenar todos os dados disponíveis.
for ano in list(range(1970, 2025)):
    # captura os dados da página.
    dados = obter_dados_processamento(ano)
    # adiciona os dados na lista.
    lista.append(dados)
    print(f'{ano}: Adicionado à lista')
print('Dados inseridos com sucesso.')
# salva a colecao de dados na pasta de destino no formato json.
salvar_arquivo(lista, caminho='./data/collections_processamento.json')

# retorno para o usuário
print('Arquivo salvo na pasta de destino.')
