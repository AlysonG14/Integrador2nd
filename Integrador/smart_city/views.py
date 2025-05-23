from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import (Ambientes, 
                     Historico, 
                     Sensores)
from .serializers import (AmbienteSerializer,
                          HistoricoSerializer,
                          SensorSerializer)
from .paginations import MyLimitOffsetPagination
from .permissions import (IsSensor,
                          IsHistorico,
                          IsAmbiente)
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.views import APIView

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'all_itens': '/'
    }

    return Response(api_urls)

class AmbienteList(ListAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbienteSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsAmbiente] 


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
            Response('Ambiente excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)
            return Response('Ambiente não encontrado', status=status.HTTP_404_NOT_FOUND)

class HistoricoList(ListAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsHistorico]

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
            Response('Histórico excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)
            return Response('Histórico não encontrado!', status=status.HTTP_404_NOT_FOUND)

class SensorList(ListAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensorSerializer
    pagination_class = MyLimitOffsetPagination
    permission_classes = [IsSensor]


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
            Response('Sensor excluído com sucesso!', status=status.HTTP_204_NO_CONTENT)
            return Response('Sensor não encontrado', status=status.HTTP_404_NOT_FOUND)
    
class CustomTokenObtainPairSerializer(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass

class RegisterView(APIView):
    permission_classes = [AllowAny]

def authenticationJWT(self, request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            json = serializer.data
            return Response(json.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
