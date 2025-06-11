from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Sensores, Historico, Ambientes, UsuarioCadastro

    
# Vamos criar um serializer, com três classes da models, para validar os dados em JSON

# Serializar para os modelos de 'Sensores'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensores
        fields = '__all__' # Isso permite que vai pegar todos os campos do Modelo
        read_only_fields = ['id'] # isso permite que o id seja sobrescrito em requisições POST ou PATCH


# Serializer para os modelos de 'Ambientes'

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambientes 
        fields = '__all__' # Isso permite que vai pegar todos os campos do Modelo
        read_only_fields = ['id'] # isso permite que o id seja sobrescrito em requisições POST ou PATCH

# Serializer para os modelos de 'Histórico' com 'timestamp' configurado para facilitar a busca de pesquisa

class HistoricoSerializer(serializers.ModelSerializer):
    # Campos adicionais calculados com base no 'timestamp'
    data = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()

    class Meta:
        model = Historico
        fields = '__all__' # Isso permite que vai pegar todos os campos do Modelo
        read_only_fields = ['id'] # isso permite que o id seja sobrescrito em requisições POST ou PATCH

    # Retorna a data do 'timestamp'
    def get_data(self, obj):
        return obj.timestamp.date()

    # Retorna a hora do 'timestamp'
    def get_hora(self, obj):
        return obj.timestamp.time().strftime('%H:%M:%S')
    
    
# Com base no método que iremos criar, vamos implementar o serializer do Token, porque conseguimos adicionar o 'payload' do token
# Payload -> É a parte que contém os dados válidos de um usuário registrado no Banco de Dados apartir de Login/Cadastro

# Define uma classe onde obtém o token padrão do SimpleJWT, 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # adicionando o email do usuário ao token,
        token = super().get_token(user) 
        token['email'] = user.email
        # adiciona a lista de grupos.
        token['roles'] = list(user.groups.values_list('name', flat=True)) # Adiciona mais reivindicações, ou seja, permite que você adicione funções usuário 
        return token # retorna o token
    
# Serializer para cadastro de usuário, incluindo validação e criação
    
class CustomUsuarioCadastrado(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True) # write_only para que não seja enviado no response

# Campos que serão expostos no serializer do Usuário Cadastro

    class Meta:
        model = UsuarioCadastro
        fields = ('nome', 'username', 'email', 'idade')

    # Método para criar um usuário usando o create_user para lidar com senha corretamente

    def create(self, validated_data):
        user = UsuarioCadastro.objects.create_user(
            # Campos necessários para validação de data
            email=validated_data['email'],
            nome=validated_data['nome'],
            username=validated_data['username'],
            idade=validated_data['idade']
        )
        return user
    

