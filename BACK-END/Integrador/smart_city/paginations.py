from rest_framework.pagination import LimitOffsetPagination

# Essa é uma classe personalizada para criar uma Paginação do DRF

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5 # Define o limite
    limit_query_param = 'mylimit' # Nome do parâmetro, para quantos itens retornar
    offset_query_param = 'myoffset' # Nome do parâmetro, para qual item começar
    max_limit = 10 # Limite máximo