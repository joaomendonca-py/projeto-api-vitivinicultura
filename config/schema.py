# construir a função schema que retorna os dados do banco de dados nas rotas post  
def all_data(lista):
    return [data_collection(element) for element in lista]
