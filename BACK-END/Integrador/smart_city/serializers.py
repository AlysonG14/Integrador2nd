from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Sensores, Historico, Ambientes, UsuarioCadastro


# Com base no método que iremos criar, vamos implementar o serializer do Token, porque conseguimos
# adicionar o 'payload' do token
# payload -> É a parte que contém os dados válidos de um usuário registrado no Banco de Dados apartir de Login/Cadastro
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['roles'] = list(user.groups.values_list('name', flat=True)) # Adiciona mais reivindicações, ou seja, permite que você adicione funções de usuário 
        return token
    
class CustomUsuarioCadastrado(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)    

    class Meta:
        model = UsuarioCadastro
        fields = ('name', 'username', 'email', 'idade')

    def create(self, validated_data):
        user = UsuarioCadastro.objects.create_user(
            email=validated_data['email'],
            name=validated_data['nome'],
            username=validated_data['username'],
            idade=validated_data['idade']
        )
        return user
    
# Vamos criar um serializer, com três classes da models, para validar os dados em JSON

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

