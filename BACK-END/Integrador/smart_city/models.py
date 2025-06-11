from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django import forms
from django_filters import rest_framework as filters

# Create your models here.

# Define os tipos possíveis de sensores (choices para o campo sensor)

TIPOS_SENSORES = [
    ('L', 'Luminosidade'),
    ('C', 'Contador'),
    ('T', 'Temperatura'),
    ('U', 'Umidade'),
]

# Aqui vai ser o campo do modelo Sensors

class Sensores(models.Model):
    sensor = models.CharField(max_length=1, choices=TIPOS_SENSORES, null=True, blank=True)
    mac_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    unidade_medida = models.CharField(max_length=255, null=True, blank=True)
    valor = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

# Campo de Nome de admim, para identificação simples

    def __str__(self):
        return f'{self.sensor}'
    
    class Meta:
        verbose_name = 'sensor'
        verbose_name_plural = 'Sensores'

# Aqui vai ser o campo de modelos ambientes (inclusive para pegar o local e a descrição)

class Ambientes(models.Model):
    sig = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    ni = models.CharField(max_length=255, null=True, blank=True)
    responsavel = models.CharField(max_length=255, null=True, blank=True)

    # Define o nome do campo de admin, para uma identificação simples

    def __str__(self):
        return f'{self.ni}' # Exibe o NI do ambiente como o principal identificação simples
    
    class Meta:
        verbose_name = 'ambiente'
        verbose_name_plural = 'Ambientes'

    # Aqui vai ser o campo dos modelos de Histórico (onde, vai validar as chaves primárias para o campo de Sensores e Ambientes)

class Historico(models.Model):
    sensor = models.ForeignKey('Sensores', on_delete=models.CASCADE, null=True, blank=True) # Valida para relacionar as duas tabelas
    ambiente = models.ForeignKey('Ambientes', on_delete=models.CASCADE, null=True, blank=True)
    valor = models.BigIntegerField()
    timestamp = models.DateTimeField()
    observacoes = models.TextField(max_length=300, null=True, blank=True)

    # Campo para identificação simples

    def __str__(self):
        return f'{self.sensor}'
    
    class Meta:
        verbose_name = 'historico'
        verbose_name_plural = 'Históricos'

# Esse campo de filters, ele vai facilitar a busca de pesquisa pelo campo da data: 'timestamp'

class HistoricoFilter(filters.FilterSet):
    data = filters.DateFilter(field_name='timestamp', lookup_expr='date')

    class Meta:
        model = Historico
        fields = ['data']

# Define os tipos possíveis de sensores (choices para o campo do Usuário Cadastrado)

DADOS_SENSORES = [
    ('S', 'Sensores'),
    ('A', 'Ambientes'),
    ('H', 'Histórico')
]

# Campo necessários para o supervisor realizar o cadastramento do sistema de Smart City, utilizando o AbstractUser

class UsuarioCadastro(AbstractUser):
    dados_sensores = models.CharField(max_length=1, choices=DADOS_SENSORES, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    idade = models.PositiveIntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    # O primeiro registro, será o email como o principal default, para o usuário fazer login através de 'login'
    USERNAME_FIELD = 'email'
    # Segunda coisa, é que ele exige um campo obrigatório de 'username' para criação
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class UploadFileForms(forms.Form):
    file = forms.FileField()