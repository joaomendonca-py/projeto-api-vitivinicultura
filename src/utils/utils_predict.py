import sys
sys.path.append('../projeto-api-vitivinicultura')
def gerar_variaveis_dummy_produto(df_input):
    """
    Gera colunas dummy para os produtos com base na lista de produtos padrão.

    Parâmetros:
    - df_input: DataFrame contendo a coluna 'produto' com o nome do produto informado pelo usuário.
    - lista_produtos: Lista de strings com todos os nomes de produtos possíveis.

    Retorno:
    - DataFrame atualizado com as colunas dummy.
    """
    lista_produtos=['Espumantes', 'Suco de uva', 'Uvas frescas', 'Vinhos de mesa']
    for produto in lista_produtos:
        nome_coluna = f'produto_texto_{produto}'
        df_input[nome_coluna] = 0  # Inicializa com 0

    # Marca a coluna do produto escolhido como 1
    produto_usuario = df_input['produto'].iloc[0]

    nome_coluna_usuario = f'produto_texto_{produto_usuario}'
    if nome_coluna_usuario in df_input.columns:
        df_input[nome_coluna_usuario] = 1
    else:
        raise ValueError(f"Produto '{produto_usuario}' não reconhecido. Produtos válidos: {lista_produtos}")

    return df_input
