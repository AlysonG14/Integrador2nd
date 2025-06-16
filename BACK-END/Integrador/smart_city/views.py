import pandas as pd 
import uuid
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (Ambientes, 
                     Sensores,
                     Historico,
                     HistoricoFilter)
from .serializers import (AmbienteSerializer,
                          HistoricoSerializer,
                          SensorSerializer)
from .serializers import CustomTokenObtainPairSerializer, UsuarioCadastro
from .paginations import MyLimitOffsetPagination

# Create your views here.

# Uma view que retorna as URLs de API para facilitar consulta

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'all_itens': '/',
        'Lista de Ambiente': '/ambiente/',
        'Detalhes do Ambiente': '/ambiente/<int:pk>/',
        'Lista de Histórico': '/historico/',
        'Detalhes do Histórico': '/historico/<int:pk>/',
        'Lista de Sensores': '/sensor/',
        'Detalhes do Sensor': '/sensor/<int:pk>/'
    }

    return Response(api_urls)



                                            # 1. SENSORES 



# --- CRUD SENSORES ---

# Listagem paginada de Sensores, somente usuários autorizados podem acessar

class SensorList(ListCreateAPIView):
    queryset = Sensores.objects.all() # Um qeuryset para listar as páginas de Sensores completos
    serializer_class = SensorSerializer # Um serializer que formata API em json
    pagination_class = MyLimitOffsetPagination # Uma paginação da classe, para definir quantos APIs vão estar 
    permission_classes = [IsAuthenticated] # E uma permissão onde apenas o usuário pode autenticar a classe

# Detalhes do Sensor, onde terá: Visualizar detalhe, atualização do sensor e deletar o sensor por ID

class SensorViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Sensores.objects.all() # Um qeuryset para listar as páginas de Sensores completos usando: GET, PATCH, DELETE
    serializer_class = SensorSerializer # # Um serializer que formata API em json
    permission_classes = [IsAuthenticated] # E uma permissão onde apenas o usuário pode autenticar a classe
    
    
# ---- IMPORTAÇÃO DE DADOS SENSORES ----


# Importando e usando o Swagger para permitir que ele possa pegar o arquivo e importar
    
@swagger_auto_schema(
    method='post',  
    manual_parameters=[
        openapi.Parameter(
            'file',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='Arquivo Excel (.xlxs ou .csv)'
        )
    ]
)

# Upload de arquivo EXCEL ou CSV para importar sensores.

@api_view(['POST']) # Criação para dar o upload do arquivo via POST
@parser_classes([MultiPartParser]) # É um método que vai aceitar as requisições dos 'upload de arquivos'
@permission_classes([IsAuthenticated]) # Autenticar que apenas o usuário cadastrado pode alterar e mudar 

# Criação de função para importar dados
def upload_sensores_api(request):

    # Verifica se o arquivo foi enviado, se não ele vai retornar a mensagem abaixo
    if 'file' not in request.FILES:
        return Response(
            {'error': 'Nenhum arquivo enviado. Use o campo "file" para enviar o arquivo Excel.'},
            status=status.HTTP_400_BAD_REQUEST
        )   
    
    # Verifica se o arquivo é excel ou CSV, se não, ele vai retornar a mensagem abaixo

    file = request.FILES['file']
    if not file.name.endswith(('.xlsx', '.csv')):
        return Response(
            {'error': 'Formato de arquivo inválido. Envia um arquivo excel (.xslx ou .csv)'},
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE # Significa que o servidor se recusa a aceitar um pedido de navegador
        )
    try:

        # Lê o arquivo com Pandas
        df = pd.read_excel(file)

        # Verifica colunas obrigatórias, se não, significa que a coluna obrigatória está em falta
        required_columns = {'sensor', 'mac_address', 'unidade_medida', 'latitude', 'longitude', 'status'}
        if not required_columns.issubset(df.columns): # Issubset -> Ferramenta robusta para verificar a relação de subconjuntos entre conjuntos.
            missing = required_columns - set(df.columns) # Uma variável para verificar quais colunas obrigatórios estão faltando
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY # Significa que ele vai fazer o servidor entender, mas não vai conseguir processar.
            )

        # Cria as requisições para mostrar o status da importação, se foi criado, atualizado ou erros.
        created_count = 0
        duplicates = 0
        errors = 0

        # Vai iterar linha à linha para criar ou atualizar sensores
        
        for _, row in df.iterrows(): # Itera sobre cada linha do DateFrame carregado do arquivo Excel
            try:
                row = row.where(pd.notnull(row), None) # Substitua valores NaN por None

                # Campos que serão atualizados ou definidos, abaixo:
                Sensores.objects.create(
                        mac_address=row['mac_address'],
                        sensor= row['sensor'],
                        unidade_medida= row['unidade_medida'],
                        latitude= row.get('latitude'),
                        longitude= row['longitude'],
                        status= row['status'],
                        timestamp= row.get('timestamp', datetime.now())
                )   
                created_count += 1 # Incrementar o contador de novos sensores criados.

            except IntegrityError as e: # Essa parte é um bloco de tratamento de erros, vai usar para incrementar o loop que insere dados no banco
                print(f"Erro ao integridade na linha {row}: {e}")
                errors += 1
                continue

        # Retorna o Response para mostrar as estatísticas detalhadas, mensagem, quantas foram atualizados, criados e falharam

        return Response(
            {
                'message': 'Importação concluída com sucesso!',
                'stats': {
                    'total_rows': len(df),
                    'created': created_count,
                    'updated': duplicates,
                    'errors': errors
                }

            },
            status=status.HTTP_201_CREATED

        )

    # Except que específica caso o arquivo esteja vazio
    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'O arquivo excel está vazio'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    # Except que expecífica caso o arquvo com erro
    except Exception as e:
        return Response(
            {'error': f'Erro ao processar arquivo: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

                                                 # 2. AMBIENTE
    
# --- CRUD AMBIENTES ---

# Listagem paginada de Ambiente, somente usuários autorizados podem acessar

class AmbienteList(ListCreateAPIView):
    queryset = Ambientes.objects.all() # Um qeuryset para listar as páginas de Ambientes completos
    serializer_class = AmbienteSerializer # Um serializer que formata API em json
    pagination_class = MyLimitOffsetPagination # Uma paginação da classe, para definir quantos APIs vão estar 
    permission_classes = [IsAuthenticated] # E uma permissão onde apenas o usuário pode autenticar a classe


class AmbienteDetailView(RetrieveUpdateDestroyAPIView): # Detalhes do Ambiente, onde terá: Visualizar detalhe de cada ambiente, atualização do ambiente e deletar o ambiente por ID
    queryset = Ambientes.objects.all() # Um qeuryset para listar as páginas de Ambiente completo usando: GET, PATCH, DELETE
    serializer_classes = AmbienteSerializer # Um serializer que formata API em json
    permission_classes = [IsAuthenticated] # E uma permissão para permitir que somente usuário cadastrado tem acessibilidade de alterar mudanças e autenticar a classe

# --- IMPORTAÇÃO DE DADOS AMBIENTES ---

# O schema do swagger -> Para permitir que ele vai importar os arquivos de Excel (.xslx ou .csv)

@swagger_auto_schema(
    method='post',  
    manual_parameters=[
        openapi.Parameter(
            'file',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='Arquivo Excel (.xlsx ou .csv)'
        )
    ]
)

# Upload de arquivo EXCEL ou CSV para importar ambientes.

@api_view(['POST']) # Criação para dar o upload do arquivo via POST
@parser_classes([MultiPartParser]) # É um método que vai aceitar as requisições dos 'upload de arquivos'
@permission_classes([IsAuthenticated]) # Autenticar que apenas o usuário cadastrado pode alterar e mudar 
def upload_ambiente_api(request):

    # Criação de função para importar dados.

    if 'file' not in request.FILES: # Verifica se o arquivo foi enviado, se não ele vai retornar a mensagem abaixo.
        return Response(
            {'error': 'Nenhum arquivo enviado. Use o campo "file" para enviar o arquivo Excel.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try: # Um método para tentar o arquivo
        file = request.FILES['file'] # Verifica se o arquivo é excel ou CSV, se não, ele vai retornar a mensagem abaixo.
        if not file.name.endswith(('.xlsx', '.csv')):
            return Response(
                {'error': 'Formato de arquivo inválido. Envie um arquivo Excel (.xlsx ou .csv)'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE # Significa que o servidor se recusa a aceitar um tipo de mídia.

            )
        
        # Lê o arquivo com Pandas.

        df = pd.read_excel(file)


        # Verifica colunas obrigatórias, se não, significa que a coluna obrigatória está em falta.
        required_columns = {'sig', 'descricao', 'ni', 'responsavel'}
        if not required_columns.issubset(df.columns): # Issubset -> Ferramenta robusta para verificar a relação de subconjuntos entre conjuntos.
            missing = required_columns - set(df.columns) # Uma variável para verificar quais colunas obrigatórios estão faltando.
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY # Significa que ele vai fazer o servidor entender, mas não vai conseguir processar.
            )
        
        # Cria as requisições para mostrar o status da importação, se foi criado, atualizado ou erros.

        created_count = 0
        duplicates = 0
        errors = 0

        # Vai iterar linha à linha para criar ou atualizar sensores

        for _, row in df.iterrows(): # Itera sobre cada linha do DateFrame carregado do arquivo Excel
            try:
                row = row.where(pd.notnull(row), None) # Substitua valores NaN por None

                # Campos que serão atualizados ou definidos, abaixo:

                Ambientes.objects.create(
                        sig=row['sig'],
                        descricao= row['descricao'],
                        ni= row.get('ni'),
                        responsavel= row.get('responsavel')
                )
                created_count += 1 # Incrementar o contador de novos sensores criados.

            except IntegrityError as e: # Essa parte é um bloco de tratamento de erros, vai usar para incrementar o loop que insere dados no banco
                print(f"Erro ao integridade na linha {row}: {e}")
                errors += 1
                continue

        # Retorna o Response para mostrar as estatísticas detalhadas, mensagem, quantas foram atualizados, criados e falharam.

        return Response(
            {
                'message': f'Importação concluído com sucesso!',
                'stats': {
                    'total_rows': len(df),
                    'created': created_count,
                    'updated': duplicates,
                    'errors': errors
                }
            },
            status=status.HTTP_201_CREATED
        )


    # Except que específica caso o arquivo esteja vazio.
    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'O arquivo excel está vazio'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    

    # Except que expecífica caso o arquvo com erro.
    except Exception as e:
        return Response(
            {'error': f'Erro ao processar arquivo: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

                                               # 3. Histórico

# --- CRUD de ListCreate do HISTÓRICO ---

# Listagem paginada de Historico, somente usuários autorizados podem acessar

class HistoricoList(ListCreateAPIView):
    queryset = Historico.objects.all() # Um queryset para listar todas as informações do Histórico
    serializer_class = HistoricoSerializer # Um serializer que formata API em json
    pagination_class = MyLimitOffsetPagination # Uma paginação da classe, para definir quantos APIs vão estar 
    permission_classes = [IsAuthenticated] # Uma permissão onde apenas o usuário pode autenticar a classe

    # --- FILTRO DE HISTÓRICO ---
    # Para filtrar a página de HistoricoList

    # Uma função de queryset para pegar as informações do Histórico e transformar ela em filtros pela busca de pesquisa poderosa!
    def get_queryset(self):
        queryset = Historico.objects.all() # Começa pegando todos os registros da tabela Histórico
        sensor_id = self.request.query_params.get('sensor_id') # Filtra a URL dos ID de sensores
        tipo_sensor = self.request.query_params.get('tipo') # Filtra a URL aos tipos de sensores
        data = self.request.query_params.get('data') # Filtra a URL da data dos sensores
        sig = self.request.query_params.get('sig') # Filtra a URL ao tipo 'SIG' dos sensores
        historico_id = self.request.query_params.get('historico_id') # Filtra a URL para pegar o ID do histórico

        # Se o sensor_id foi passado, então filtra os históricos daquele sensor
        if sensor_id:
            queryset = queryset.filter(sensor__id=sensor_id)

        # Se o tipo de sensor foi passado, então filtra daquele que contém tipo de sensores, tipo: "temperatura"

        if tipo_sensor:
            queryset = queryset.filter(sensor__sensor__icontains=tipo_sensor)

        # Se a data foi passado, então filtra a data específica do sensor

        if data:
            queryset = queryset.filter(timestamp__date=data)

        # Se o tipo 'sig' foi passado, então vai filtrar esse tipo de "sig" no sensor

        if sig:
            queryset = queryset.filter(ambiente__sig__iexact=sig)

        # Se o ID do histórico foi passado, então ele vai filtrar exatamente o ID do histórico

        if historico_id:
            queryset = queryset.filter(id=historico_id)

        # Retorna a queryset filtrado de acordo com os parâmetros fornecidos
        return queryset
    
# --- CRUD de GET, PATCH, DELETE --- 

class HistoricoViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Historico.objects.all() # Um queryset para listar todas as informações do Histórico, usando: GET, PATCH, DELETE
    serializer_class = HistoricoSerializer # Um serializer que formata API em json
    permission_classes = [IsAuthenticated] # E Uma paginação da classe, para definir quantos APIs vão estar 

# --- IMPORTAÇÃO DE DADOS HISTÓRICOS --- 
    
# O schema do swagger -> Para permitir que ele vai importar os arquivos de Excel (.xslx ou .csv)
    
@swagger_auto_schema(
    method='post',  
    manual_parameters=[
        openapi.Parameter(
            'file',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='Arquivo Excel (.xlxs ou .csv)'
        )
    ]
)

# Upload de arquivo EXCEL ou CSV para importar históricos.
 
@api_view(['POST']) # Criação para dar o upload do arquivo via POST
@parser_classes([MultiPartParser]) # É um método que vai aceitar as requisições dos 'upload de arquivos'
@permission_classes([IsAuthenticated]) # Autenticar que apenas o usuário cadastrado pode alterar e mudar
def upload_historico_api(request):

    # Criação de função para importar dados.
    if 'file' not in request.FILES: # Verifica se o arquivo foi enviado, se não ele vai retornar a mensagem abaixo.
        return Response(
            {'error': 'Nenhum arquivo enviado. Use o campo "file" para enviar o arquivo Excel.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        file = request.FILES['file'] 

        if not file.name.endswith(('.xlsx', '.csv')): # Verifica se o arquivo é excel ou CSV, se não, ele vai retornar a mensagem abaixo.
            return Response(
                {'error': 'Formato de arquivo inválido. Envie um arquivo Excel (.xlsx ou .csv)'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE # Significa que o servidor se recusa a aceitar um pedido de navegador.
            )

        # Lê o arquivo com Pandas.
        df = pd.read_excel(file)

        # Verifica colunas obrigatórias, se não, significa que a coluna obrigatória está em falta.
        required_columns = {'sensor', 'ambiente', 'valor', 'timestamp'}
        if not required_columns.issubset(df.columns): # Issubset -> Ferramenta robusta para verificar a relação de subconjuntos entre conjuntos.
            missing = required_columns - set(df.columns) # Uma variável para verificar quais colunas obrigatórios estão faltando.
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY # Significa que ele vai fazer o servidor entender, mas não vai conseguir processar.
            )
        
        # Cria as requisições para mostrar o status da importação, se foi criado, atualizado ou erros.
        created_count = 0
        duplicates = 0
        errors = 0

        # Vai iterar linha à linha para criar ou atualizar sensores

        for _, row in df.iterrows(): # Itera sobre cada linha do DateFrame carregado do arquivo Excel
            try:  
                row = row.where(pd.notnull(row), None) # Substitua valores NaN por None

                # Essa parte, vai pegar os valores da linha do Excel que precisamos no Banco de Dados
                
                sensor_id = int(row['sensor']) # Pega o valor 'sensor' da linha Excel e converte para inteiro (que espera o ID)
                ambiente_id = int(row['ambiente']) # Pega o valor 'ambiente' da linha Excel e converte para inteiro (que também espera o ID)

                sensor = Sensores.objects.filter(id=sensor_id).first() # Busca no banco de dados o 'sensor' correspondente ao ID informado
                ambiente = Ambientes.objects.filter(id=ambiente_id).first() # Busca no banco de dados o 'ambiente' correspondente ao ID informado

                # Verifica se o 'sensor' não foi encontrado no bando (informado ao ID)
                if not sensor:
                    print(f"Sensor não encontrado: '{row['sensor']}'")

                # Verifica se o 'ambiente' não foi encontrado no bando (informado ao ID)
                if not ambiente:
                    print(f"Ambiente não encontrado: '{row['ambiente']}'")

                if not sensor or not ambiente: # Se qualquer um dos dois não exitir na linha do Excel (informado pelo ID), então:
                    errors += 1 # Incrementa o contador de erros
                    continue # Pula para próxima linha da planilha, sem tentar criar ou atualizar nada

                # Campos que serão atualizados ou definidos, abaixo:

                Historico.objects.create(
                        sensor=sensor,
                        ambiente=ambiente,
                        valor=row['valor'],
                        timestamp=pd.to_datetime(row['timestamp']),
                        observacoes=row.get('observacoes') or ''
                )
                created_count += 1 # Incrementar o contador de novos sensores criados.

            except Exception as e: # Essa parte é um bloco de tratamento de erros, vai usar para incrementar o loop que insere dados no banco
                print(f'Erro ao importar linha: {e}')
                errors += 1
                continue
        
        # Retorna o Response para mostrar as estatísticas detalhadas, mensagem, quantas foram atualizados, criados e falharam.
        return Response(
            {
                'message': f'Importação concluído com sucesso!',
                'stats': {
                    'total_rows': len(df),
                    'created': created_count,
                    'updated': duplicates,
                    'errors': errors
                }
            },
            status=status.HTTP_201_CREATED
        )


    # Except que específica caso o arquivo esteja vazio.
    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'O arquivo excel está vazio'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    # Except que expecífica caso o arquvo com erro.
    except Exception as e:
        return Response(
            {'error': f'Erro ao processar arquivo: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    

                                        #4. UsuárioCadastro


class CustomTokenObtainPairView(TokenObtainPairView): # Esse método manipula uma criação de tokens de acesso ao login
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView): # Esse método é responsável por atualizar tokens de acesso ao usuário
    pass

class RegisterView(APIView): # Esse método, permite que os novos usuários se registrem a partir da permissions classes
    permission_classes = [AllowAny]

    # Vamos criar uma request que os dados serão enviados via POST através do serializer

    def post(self, request):
        serializer = UsuarioCadastro(data= request.data) # Serializa os dados enviados via POST
        if serializer.is_valid(): # Se o serializer é válido, então...
            user = serializer.save() # Salva o novo usuário no Banco de Dados
            if user: # Se o usuário, vai...
                json = serializer.data # Preparar a resposta com os dados do novo usuário, então...
                return Response(json, status=status.HTTP_201_CREATED) # Vai receber essa mensagem, criado!
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) # Ou receberá essa mensagem de erro.

# Uma classe para aumentar a segurança da View

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated] # Apenas os usuários logados podem acessar

    # Retorna a mensagem, protegido, caso se o usuário verá essa mensagem!
    def get(self, request):
        return Response({'message':'This field is protected.'}) 


def export_smartcity_to_excel(request):
    ambiente = pd.DataFrame(list(Ambientes.objects.all().values()))
    historico = pd.DataFrame(list(Historico.objects.all().values()))
    sensor = pd.DataFrame(list(Sensores.objects.all().values()))

    if 'timestamp' in historico.columns:
        historico['timestamp'] = pd.to_datetime(historico['timestamp']).dt.tz_localize(None)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=smartcity.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        ambiente.to_excel(writer, sheet_name='Ambientes', index=False)
        historico.to_excel(writer, sheet_name='Historico', index=False)
        sensor.to_excel(writer, sheet_name='Sensores', index=False)

    return response

# Uma classe para exportação de dados de todos os registros

class ExportFileExcel(APIView):
    def queryset(self, request):
        sensores = Sensores.objects.all()
        serializerSensores = SensorSerializer(sensores, many=True)
        df = pd.DataFrame(serializerSensores.data)
        df.to_csv(f"public/static/excel/{uuid.uuid4()}.csv", encoding="UTF-8")
        print(df)

        return Response({'status': 200})

    def queryset(self, request):
        sensores = Sensores.objects.all()
        serializerSensores = SensorSerializer(sensores, many=True)
        df = pd.DataFrame(serializerSensores.data)
        df.to_csv(f"public/static/excel/{uuid.uuid4()}.csv", encoding="UTF-8")
        print(df)

        return Response({'status': 200})
    
    def queryset(self, request):
        sensores = Sensores.objects.all()
        serializerSensores = SensorSerializer(sensores, many=True)
        df = pd.DataFrame(serializerSensores.data)
        print(df)

        return Response({'status': 200})
