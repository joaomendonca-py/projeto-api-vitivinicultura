""" Arquivo de funções executadas nas apis"""
import sys
import requests
from bs4 import BeautifulSoup
sys.path.append('../projeto-api-vitivinicultura')
from config.models import ImportacaoExportacao

# função api Importação e Exportação
def obter_dados_import_export(ano:int, derivado:str, processo:str, tag_page:str):
    ''' Função que executa o scrapping de dados da página Importação ou Exportação.'''

    # Lista para armazenar os dados
    lista_registros = []      
    # link de acesso com os parâmetros de filtro
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&\
    opcao=opt_{tag_page}&subopcao=subopt_{derivado}'

    # conexão com a página html.
    response = requests.get(url, timeout=200)

    # construção do objeto Beautifulsoap e análise da página html.
    soup = BeautifulSoup(response.text, 'html.parser')

    # construção da feature tipo_uva.
    derivado_texto = soup.find(
        'button', {'class': 'btn_sopt', 'value': f'subopt_{derivado}'}).get_text(strip=True)

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
    produto = ImportacaoExportacao(ano=ano,
                            processo=processo,
                            produto=derivado,
                            produto_texto=derivado_texto,
                            labels=[label.get_text(strip=True)
                                    for label in table.find_all('th')],
                            data=lista_registros[1:]
                            )
    return dict(produto)


# função para salvamento do arquivo
def obter_dados_pagina_import_export(ano:int, processo:str, tag_page):
    ''' Função que executa o scrapping de dados da página Processamento.'''

    # verificação do processo para definir quantidade de botões na lista
    if processo == "Importação":
        # variável de filtro
        lista_derivados = ['01', '02', '03', '04','05']

    elif processo == "Exportação":
        # variável de filtro
        lista_derivados = ['01', '02', '03', '04']
    else:
        raise ValueError

    # Lista para armazenar os dados
    lista_registros = []
    lista_produtos = []

    # laço de repetição para verificar cada elemento botão da página aplicando filtro nos dados.
    for derivado in lista_derivados:

        # link de acesso com os parâmetros de filtro
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&\
        opcao=opt_{tag_page}&subopcao=subopt_{derivado}'

        # conexão com a página html.
        response = requests.get(url, timeout=200)

        # construção do objeto Beautifulsoap e análise da página html.
        soup = BeautifulSoup(response.text, 'html.parser')

        # construção da feature tipo_uva.
        derivado_texto = soup.find(
            'button', {'class': 'btn_sopt', 'value': f'subopt_{derivado}'}).get_text(strip=True)

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
        produto = ImportacaoExportacao(ano=ano,
                            processo=processo,
                            produto=derivado,
                            produto_texto=derivado_texto,
                            labels=[label.get_text(strip=True)
                                    for label in table.find_all('th')],
                            data=lista_registros[1:]
                            )

        # limpa os dados da lista para reinicilizar o laço de repetição.
        lista_registros.clear()
        # converte os dados da classe no formato dicionário.
        lista_produtos.append(produto.dict())
    return lista_produtos
