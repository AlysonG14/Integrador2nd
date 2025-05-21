from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (Ambientes, 
                     Historico, 
                     Sensores)
from .serializers import (AmbienteSerializer,
                          HistoricoSerializer,
                          SensorSerializer)


# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'all_itens': '/'
    }

    return Response(api_urls)
