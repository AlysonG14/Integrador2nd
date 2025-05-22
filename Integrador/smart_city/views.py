from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import (Ambientes, 
                     Historico, 
                     Sensores)
from .serializers import (AmbienteSerializer,
                          HistoricoSerializer,
                          SensorSerializer)
from .paginations import MyLimitOffsetPagination

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
    permission_classes = MyLimitOffsetPagination




class HistoricoList(ListAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = MyLimitOffsetPagination

class SensorList(ListAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensorSerializer
    permission_classes = MyLimitOffsetPagination


