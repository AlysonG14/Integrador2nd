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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'all_itens': '/',
        'Lista de Ambiente': '/ambiente/',
        'Criação de Ambiente': '/ambiente/criar/',
        'Detalhes do Ambiente': '/ambiente/<int:pk>',
        'Lista de Histórico': '/historico/',
        'Criação de Histórico': '/historico/criar/',
        'Detalhes do Histórico': '/historico/<int:pk>',
        'Lista de Sensores': '/sensor/',
        'Criação de Sensor': '/sensor/criar',
        'Detalhes do Sensor': '/sensor/<int:pk>'
    }

    return Response(api_urls)

class SensorList(ListAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensorSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def createSensor(request):
    serializer = SensorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def sensorDetail(request, pk):
    sensor = get_object_or_404(Sensores, pk=pk)

    if request.method == 'GET':
        serializer = SensorSerializer(sensor)
        return Response(serializer.data)
        
    elif request.method == 'PATCH':
        serializer = SensorSerializer(sensor, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
            sensor.delete()
            return Response('Sensor excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def upload_sensores_api(request):
    if 'file' not in request.FILES:
        return Response(
            {'error': 'Nenhum arquivo enviado. Use o campo "file" para enviar o arquivo Excel.'},
            status=status.HTTP_400_BAD_REQUEST
        )   

    file = request.FILES['file']
    if not file.name.endswith(('.xlsx', '.csv')):
        return Response(
            {'error': 'Formato de arquivo inválido. Envia um arquivo excel (.xslx ou .csv)'},
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )
    try:
        df = pd.read_excel(file)
        required_columns = {'mac_address', 'sensor', 'unidade_medida', 'longitude', 'status'}
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

                _, created = Sensores.objects.update_or_create(
                    mac_address=row['mac_address'],
                    defaults={
                        'sensor': row['sensor'],
                        'unidade_medida': row['unidade_medida'],
                        'latitude': row.get('latitude'),
                        'longitude': row['longitude'],
                        'status': row['status'],
                        'timestamp': row.get('timestamp', datetime.now())
                    }
                )
                if created:
                    created_count += 1
                else:
                    duplicates += 1

            except Exception as e:
                errors += 1
                continue

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

class AmbienteList(ListAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbienteSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsAuthenticated] 


@api_view(['POST'])
def createAmbiente(request):
    serializer = AmbienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def ambienteDetail(request, pk):
    ambiente = get_object_or_404(Ambientes, pk=pk)

    if request.method == 'GET':
        serializer = AmbienteSerializer(ambiente)
        return Response(serializer.data)
        
    elif request.method == 'PATCH':
        serializer = AmbienteSerializer(ambiente, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
            ambiente.delete()
            return Response('Ambiente excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)

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

        required_columns = {'sig', 'descricao'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        created_count = 0
        duplicates_count = 0

        for _, row in df.iterrows():
            row = row.where(pd.notnull(row), None)

            _, created = Ambientes.objects.update_or_create(
                sig=row['sig'],
                defaults={
                    'descricao': row['descricao'],
                    'ni': row.get('ni'),
                    'responsavel': row.get('responsavel')
                }
            )
            if created:
                created_count += 1
            else:
                duplicates_count += 1

        return Response(
            {
                'message': f'Importação concluído com sucesso!',
                'stats': {
                    'total_rows': len(df),
                    'created': created_count,
                    'updated': duplicates_count
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

@api_view(['POST'])
def createHistorico(request):
    serializer = HistoricoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def historicoDetail(request, pk):
    historico = get_object_or_404(Historico, pk=pk)

    if request.method == 'GET':
        serializer = HistoricoSerializer(historico)
        return Response(serializer.data)
        
    elif request.method == 'PATCH':
        serializer = HistoricoSerializer(historico, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
            historico.delete()
            return Response('Histórico excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)
    
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
        if not file.name.endswith((".xlsx", ".csv")):
            return Response(
                {'error': 'Formato inválido'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        df = pd.read_excel(file)
        required_columns = {'sensor_id', 'ambiente_id', 'valor', 'timestamp'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            return Response(
                {'error': f'Colunas obrigatórias faltando: {", ".join(missing)}'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        created_count = 0
        error_count = 0
        
        for __, row in df.iterrows():
            try:
                row = row.where(pd.notnull(row), None)
                timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')

                Historico.objects.create(
                    sensor_id=row['sensor_id'],
                    ambiente_id=row['ambiente_id'],
                    valor=row['valor'],
                    timestamp=timestamp,
                    observacoes=row.get('observacoes', '')
                )
                created_count += 1

            except Exception as e:
                error_count += 1
                continue

        return Response(
            {
                'message': 'Dados históricos importados',
                'stats': {
                    'created': created_count,
                    'errors': error_count,
                    'total': len(df)
                }
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {'error': f'Erro ao servidor: {str(e)}' },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

    df = pd.DataFrame(())

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    response['Content-Disposition'] = 'attachment; filename=smartcity.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        ambiente.to_excel(writer, sheet_name='Ambientes', index=False)
        historico.to_excel(writer, sheet_name='Historico', index=False)
        sensor.to_excel(writer, sheet_name='Sensores', index=False)

    return response

