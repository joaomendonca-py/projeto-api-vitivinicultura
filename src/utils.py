""" Arquivo de funções executadas nas apis"""
import requests
from bs4 import BeautifulSoup
from config.models import Processamento  # type: ignore

# função api Processamento
def obter_dados_processamento(ano):
    ''' Função que executa o scrapping de dados da página Processamento.'''
    # contantes de filtro e retorno
    PROCESSO = 'Processamento'

    # variável de filtro
    lista_tipo_uva = ['01', '02', '03', '04']

    # Lista para armazenar os dados
    lista_registros = []
    lista_produtos = []

    # laço de repetição para verificar cada elemento botão da página aplicando filtro nos dados.
    for tipo_uva in lista_tipo_uva:

        # link de acesso com os parâmetros de filtro
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_{tipo_uva}'

        # conexão com a página html.
        response = requests.get(url, timeout=200)

        # construção do objeto Beautifulsoap e análise da página html.
        soup = BeautifulSoup(response.text, 'html.parser')

        # construção da feature tipo_uva.
        tipo_uva_texto = soup.find(
            'button', {'class': 'btn_sopt', 'value': f'subopt_{tipo_uva}'}).get_text(strip=True)

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
        produto = Processamento(ano=ano,
                                processo=PROCESSO,
                                tipo_uva=tipo_uva_texto,
                                labels=[label.get_text(strip=True)
                                        for label in table.find_all('th')],
                                data=lista_registros[1:]
                                )

        # limpa os dados da lista para reinicilizar o laço de repetição.
        lista_registros.clear()
        # converte os dados da classe no formato dicionário.
        lista_produtos.append(produto.dict())
    return lista_produtos
