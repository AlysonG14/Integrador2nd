import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import (Ambientes, 
                     Historico, 
                     Sensores,
                     UploadFileForms)
from .serializers import (AmbienteSerializer,
                          HistoricoSerializer,
                          SensorSerializer)
from .paginations import MyLimitOffsetPagination
from .serializers import CustomTokenObtainPairSerializer, UsuarioCadastro

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
        'Detalhes do Sensorf': '/sensor/<int:pk>'
    }

    return Response(api_urls)

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
    
def upload_file_ambiente(request):
    if request.method == 'POST':
        form = UploadFileForms(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                ambiente, created = Ambientes.objects.get_or_create(
                    sig=row['sig'],
                    descricao=row['descricao'],
                    ni=row['ni'],
                    responsavel=row['responsavel']
                )
                if created:
                    messages.success(request, f'Importado com sucesso {ambiente.sig}')
                else:
                    messages.warning(request, f'{ambiente.sig} existe!')
            return redirect('upload_file_ambiente')
    else:
        form = UploadFileForms
    return render(request, 'smart_city/importar_ambiente.html', {'form' : form})


class HistoricoList(ListAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsAuthenticated]

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
    
def upload_file_historico(request):
    if request.method == 'POST':
        form = UploadFileForms(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            for __, row in df.iterrows():
                historico, created = Historico.objects.get_or_create(
                    sensor=row['sensor'],
                    ambiente=row['ambiente'],
                    valor=row['valor'],
                    timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                )
                if created:
                    messages.success(request, f'Importado com Sucesso {historico.sensor}')
                else:
                    messages.warning(request, f'{historico.sensor} existe!')
            return redirect('upload_file_historico')
    else:
        form = UploadFileForms
    return render(request, 'smart_city/importar_historico.html', {'form': form})

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

def upload_sensores_file(request):
    if request.method == 'POST':
        form = UploadFileForms(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            for __, row in df.iterrows():
                sensor, created = Sensores.objects.get_or_create(
                    sensor=row['sensor'],
                    mac_address=row['mac_address'],
                    unidade_medida=row['unidade_medida'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    status=row['status']
                )
                if created:
                    messages.success(request, f'Importado com Sucesso {sensor.sensor}')
                else:
                    messages.warning(request, f'{sensor.sensor} não Existe')

            return redirect('upload_sensores_file')
    else:
        form = UploadFileForms
    return render(request, 'smart_city/importar_sensores.html', {'form': form})
    

class CustomTokenObtainPairSerializer(TokenObtainPairView): # Esse método manipula uma criação de tokens de acesso ao login
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

