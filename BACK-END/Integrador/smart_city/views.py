import pandas as pd 
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
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
        'Criação de Ambiente': '/ambiente/criar/',
        'Detalhes do Ambiente': '/ambiente/<int:pk>/',
        'Lista de Histórico': '/historico/',
        'Criação de Histórico': '/historico/criar/',
        'Detalhes do Histórico': '/historico/<int:pk>/',
        'Lista de Sensores': '/sensor/',
        'Criação de Sensor': '/sensor/criar/',
        'Detalhes do Sensor': '/sensor/<int:pk>/'
    }

    return Response(api_urls)

# Listagem paginada de Sensores, somente usuários autorizados podem acessar
# Um serializer que formata API em json
# Uma paginação da classe, para definir quantos APIs vão estar 
# E uma permissão onde apenas o usuário pode autenticar a classe

class SensorList(ListAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensorSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsAuthenticated]


# Criação do Sensor via POST separado

@api_view(['POST']) # Método POST -> Criar sensor
def createSensor(request):
    serializer = SensorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Detalhes do Sensor, onde terá: Visualizar detalhe, atualização do sensor e deletar o sensor por ID

@api_view(['GET', 'PATCH', 'DELETE'])
def sensorDetail(request, pk):
    sensor = get_object_or_404(Sensores, pk=pk)

    if request.method == 'GET': # Método Detalhes de cada sensor por ID
        serializer = SensorSerializer(sensor)
        return Response(serializer.data)
        
    elif request.method == 'PATCH': # Método PATCH -> Atualizar o sensor por ID
        serializer = SensorSerializer(sensor, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE': # Método DELETE -> Excluir o sensor por ID
            sensor.delete()
            return Response('Sensor excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)
    
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
@parser_classes([MultiPartParser])
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
            missing = required_columns - set(df.columns)
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY # Significa que ele vai fazer o servidor entender, mas não vai conseguir processar.
            )

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

            except IntegrityError: # 
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
    
# Listagem paginada de Ambiente, somente usuários autorizados podem acessar
# Um serializer que formata API em json
# Uma paginação da classe, para definir quantos APIs vão estar 
# E uma permissão onde apenas o usuário pode autenticar a classe

class AmbienteList(ListAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbienteSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsAuthenticated] 

# Criação de Ambiente via POST separado

@api_view(['POST']) # Método POST -> Criar ambiente
def createAmbiente(request):
    serializer = AmbienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Detalhes do Ambiente, onde terá: Visualizar detalhe de cada ambiente, atualização do ambiente e deletar o ambiente por ID

@api_view(['GET', 'PATCH', 'DELETE'])
def ambienteDetail(request, pk):
    ambiente = get_object_or_404(Ambientes, pk=pk)

    if request.method == 'GET': # Método GET -> Pegar os detalhes de cada ambiente por ID
        serializer = AmbienteSerializer(ambiente)
        return Response(serializer.data)
        
    elif request.method == 'PATCH': # Método PATCH -> Atualizar o ambiente por ID
        serializer = AmbienteSerializer(ambiente, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE': # Método DELETE -> Deletar o ambiente por ID
            ambiente.delete()
            return Response('Ambiente excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)

# O schema do swagger

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

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def upload_ambiente_api(request):
    if 'file' not in request.FILES:
        return Response(
            {'error': 'Nenhum arquivo enviado. Use o campo "file" para enviar o arquivo Excel.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        file = request.FILES['file']
        if not file.name.endswith(('.xlsx', '.csv')):
            return Response(
                {'error': 'Formato de arquivo inválido. Envie um arquivo Excel (.xlsx ou .csv)'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )

        df = pd.read_excel(file)

        required_columns = {'sig', 'descricao', 'ni', 'responsavel'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        created_count = 0
        duplicates = 0
        errors = 0

        for _, row in df.iterrows():
            try:
                row = row.where(pd.notnull(row), None)

                Ambientes.objects.create(
                        sig=row['sig'],
                        descricao= row['descricao'],
                        ni= row.get('ni'),
                        responsavel= row.get('responsavel')
                )
                created_count += 1 # Incrementar o contador de novos sensores criados.

            except IntegrityError: # 
                errors += 1
                continue

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

    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'O arquivo excel está vazio'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    except Exception as e:
        return Response(
            {'error': f'Erro ao processar arquivo: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

# Listagem paginada de Historico, somente usuários autorizados podem acessar
# Um serializer que formata API em json
# Uma paginação da classe, para definir quantos APIs vão estar 
# E uma permissão onde apenas o usuário pode autenticar a classe

class HistoricoList(ListAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    pagination_class = MyLimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_class = HistoricoFilter

    def get_queryset(self):
        queryset = Historico.objects.all()
        sensor_id = self.request.query_params.get('sensor_id')
        tipo_sensor = self.request.query_params.get('tipo')
        data = self.request.query_params.get('data')
        sig = self.request.query_params.get('sig')
        historico_id = self.request.query_params.get('historico_id')

        if sensor_id:
            queryset = queryset.filter(sensor__id=sensor_id)

        if tipo_sensor:
            queryset = queryset.filter(sensor__sensor__icontains=tipo_sensor)

        if data:
            queryset = queryset.filter(timestamp__date=data)

        if sig:
            queryset = queryset.filter(ambiente__sig__iexact=sig)

        if historico_id:
            queryset = queryset.filter(id=historico_id)

        return queryset
    
# Criação de Histórico via POST separado

@api_view(['POST']) # Método POST -> Criação de Histórico
def createHistorico(request):
    serializer = HistoricoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Detalhes do Ambiente, onde terá: Visualizar detalhe de cada ambiente, atualização do ambiente e deletar o ambiente por ID


@api_view(['GET', 'PATCH', 'DELETE'])
def historicoDetail(request, pk):
    historico = get_object_or_404(Historico, pk=pk)

    if request.method == 'GET': # Método GET -> Pegar os detalhes de cada histórico por ID
        serializer = HistoricoSerializer(historico) 
        return Response(serializer.data)
        
    elif request.method == 'PATCH': # Método PATCH -> Permite atualizar o histórico por ID
        serializer = HistoricoSerializer(historico, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE': # Método DELETE -> Exclua as informações do Histórico por ID
            historico.delete()
            return Response('Histórico excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)
    
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

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def upload_historico_api(request):
    if 'file' not in request.FILES:
        return Response(
            {'error': 'Nenhum arquivo enviado. Use o campo "file" para enviar o arquivo Excel.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        file = request.FILES['file']
        if not file.name.endswith(('.xlsx', '.csv')):
            return Response(
                {'error': 'Formato de arquivo inválido. Envie um arquivo Excel (.xlsx ou .csv)'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )

        df = pd.read_excel(file)

        required_columns = {'sensor', 'ambiente', 'valor', 'timestamp'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        created_count = 0
        duplicates = 0
        errors = 0

        for _, row in df.iterrows():
            try:
                row = row.where(pd.notnull(row), None)
                sensor_id = int(row['sensor'])
                ambiente_id = int(row['ambiente'])

                sensor = Sensores.objects.filter(id=sensor_id).first()
                ambiente = Ambientes.objects.filter(id=ambiente_id).first()

                if not sensor:
                    print(f"Sensor não encontrado: '{row['sensor']}'")
                if not ambiente:
                    print(f"Ambiente não encontrado: '{row['ambiente']}'")

                if not sensor or not ambiente:
                    errors += 1
                    continue

                Historico.objects.create(
                        sensor=sensor,
                        ambiente=ambiente,
                        valor=row['valor'],
                        timestamp=pd.to_datetime(row['timestamp']),
                        observacoes=row.get('observacoes') or ''
                )
                created_count += 1 # Incrementar o contador de novos sensores criados.

            except Exception as e:
                print(f'Erro ao importar linha: {e}')
                errors += 1
                continue

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

    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'O arquivo excel está vazio'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    except Exception as e:
        return Response(
            {'error': f'Erro ao processar arquivo: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomTokenObtainPairView(TokenObtainPairView): # Esse método manipula uma criação de tokens de acesso ao login
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView): # Esse método é responsável por atualizar tokens de acesso ao usuário
    pass

class RegisterView(APIView): # Esse método, permite que os novos usuários se registrem a partir da permissions classes
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioCadastro(data= request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

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

