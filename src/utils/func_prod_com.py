""" Arquivo de funções da api de Produção."""
import sys
import requests
from bs4 import BeautifulSoup
sys.path.append('../projeto-api-vitivinicultura')
from config.models import ProducaoComercializacao

# função api Produção e Comercialização
def obter_dados_prod_com(ano:int, processo:str, tag_page=str):
    ''' Função que executa o scrapping de dados da página Produção e Comercialização.'''

    # Lista para armazenar os dados
    lista_registros = []

    # link de acesso com os parâmetros de filtro
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&\
    opcao=opt_{tag_page}'

    # conexão com a página html.
    response = requests.get(url, timeout=200)

    # construção do objeto Beautifulsoap e análise da página html.
    soup = BeautifulSoup(response.text, 'html.parser')

    # encontra a tabela específica pela classe
    table = soup.find('table', {'class': 'tb_base tb_dados'})

    # extrai as linhas da tabela
    rows = table.find_all('tr')

    # Itera sobre as linhas e extrai o texto das células
    for row in rows:
        # pesquisa dos elementos de td: itens e sub_items.
        cells = row.find_all('td')
        cells_text = [cell.get_text(strip=True) for cell in cells]
        # construção da feature data
        lista_registros.append(cells_text)

    # Cria um produto resultante da iteração
    produto = ProducaoComercializacao(ano=ano,
                            processo=processo,
                            labels=[label.get_text(strip=True)
                                    for label in table.find_all('th')],
                            data=lista_registros[1:]
                            )
    return dict(produto)
