from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Sensores:
    sensor = models.CharField(max_length=255, null=True, blank=True)
    mac_address = models.CharField(max_length=255, null=True, blank=True)
    unidade_mad = models.CharField(max_length=255, null=True, blank=True)
    valor = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.sensor}'
    
    class Meta:
        verbose_name = 'sensor'
        verbose_name_plural = 'Sensores'


class Ambientes:
    sig = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    ni = models.CharField(max_length=255, null=True, blank=True)
    responsavel = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.ni}'
    
    class Meta:
        verbose_name = 'ambiente'
        verbose_name_plural = 'Ambientes'

class Historico:
    sensor = models.ForeignKey('Sensores', on_delete=models.CASCADE, null=True, blank=True)
    ambiente = models.ForeignKey('Ambientes', on_delete=models.CASCADE, null=True, blank=True)
    observacoes = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.sensor}'
    
    class Meta:
        verbose_name = 'historico'
        verbose_name_plural = 'Históricos'


DADOS_SENSORES = [
    ('S', 'Sensores'),
    ('A', 'Ambientes'),
    ('H', 'Histórico')
]

class UsuarioCadastro(AbstractUser):
    id = models.IntegerField(null=True, blank=True)
    dados_sensores = models.CharField(max_length=1, choices=DADOS_SENSORES, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    senha = models.CharField(max_length=255)
    idade = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name