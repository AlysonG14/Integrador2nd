from rest_framework import serializers
from .models import Sensores, Historico, Ambientes

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensores
        fields = '__all__'
        read_only_fields = ['id'] # isso permite que o id seja sobrescrito em requisições POST ou PATCH

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'
        read_only_fields = ['id']

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambientes
        fields = '__all__'
        read_only_fields = ['id']

