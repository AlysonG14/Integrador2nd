from django.db import models # Importação de funcionamento dos modelos
from django.core.validators import RegexValidator # Importação de Validação
from django.contrib.auth.models import AbstractUser # Importação de cadastramento de usuário do sistema
from django import forms # Importação de Formulário
from django_filters import rest_framework as filters # Importação de Filtros

# Create your models here.

# Define os tipos possíveis de sensores (choices para o campo sensor)

TIPOS_SENSORES = [
    ('Luminosidade', 'Luminosidade'),
    ('Contador', 'Contador'),
    ('Temperatura', 'Temperatura'),
    ('Umidade', 'Umidade'),
]

# Define o 'STATUS' do sensor para mostrar se está ativo ou inativo

STATUS = [
    ('Ativo', 'Ativo'),
    ('Inativo', 'Inativo')
]

# Define tipo de unidade do sensor

TIPO_UNIDADE = [
    ('C°', '°C'),
    ('%', '%'),
    ('uni', 'uni'),
    ('lux', 'lux')
]

# Aqui vai ser o campo do modelo Sensores

class Sensores(models.Model):
    sensor = models.CharField(max_length=12, choices=TIPOS_SENSORES, null=True, blank=True)
    mac_address = models.CharField(max_length=255, null=True, blank=True)
    unidade_medida = models.CharField(max_length=3, choices=TIPO_UNIDADE, null=True, blank=True)
    valor = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

# Campo de Nome de admim, para identificação simples

    def __str__(self):
        return f'{self.sensor} - {self.mac_address}'
    
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
        return f'{self.descricao}' # Exibe a 'descricao' do ambiente como o principal identificação simples
    
    class Meta:
        verbose_name = 'ambiente'
        verbose_name_plural = 'Ambientes'

    # Aqui vai ser o campo dos modelos de Histórico (onde, vai validar as chaves primárias para o campo de Sensores e Ambientes)

class Historico(models.Model):
    sensor = models.ForeignKey('Sensores', on_delete=models.CASCADE, null=True, blank=True) # Valida para relacionar a tabela 'sensor'
    ambiente = models.ForeignKey('Ambientes', on_delete=models.CASCADE, null=True, blank=True) # Valida para relacionar a tabela 'ambiente'
    valor = models.IntegerField(null=False, blank=False)
    timestamp = models.DateTimeField()
    observacoes = models.TextField(max_length=300, null=True, blank=True)

    # Campo para identificação simples

    def __str__(self):
        return f'{self.sensor} - {self.ambiente}'
    
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

class UsuarioCadastro(AbstractUser):
    nome = models.CharField(max_length=255, null=True, blank=True)
    pais = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    senha = models.CharField(max_length=255)

    # O primeiro registro, será o email como o principal default, para o usuário fazer login através de 'login'
    USERNAME_FIELD = 'email'
    # Segunda coisa, é que ele exige um campo obrigatório de 'username' para criação
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
# Uma classe para importação de dados de todos os registros
    
class UploadFileForms(forms.Form):
    file = forms.FileField()
