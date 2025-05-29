from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your models here.

TIPOS_SENSORES = [
    ('L', 'Luminosidade'),
    ('C', 'Contador'),
    ('T', 'Temperatura'),
    ('U', 'Umidade'),
]

class Sensores(models.Model):
    sensor = models.CharField(max_length=1, choices=TIPOS_SENSORES, null=True, blank=True)
    mac_address = models.CharField(max_length=255, null=True, blank=True)
    unidade_medida = models.CharField(max_length=255, null=True, blank=True)
    valor = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.sensor}'
    
    class Meta:
        verbose_name = 'sensor'
        verbose_name_plural = 'Sensores'


class Ambientes(models.Model):
    sig = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    ni = models.CharField(max_length=255, null=True, blank=True)
    responsavel = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.ni}'
    
    class Meta:
        verbose_name = 'ambiente'
        verbose_name_plural = 'Ambientes'

class Historico(models.Model):
    sensor = models.ForeignKey('Sensores', on_delete=models.CASCADE, null=True, blank=True)
    ambiente = models.ForeignKey('Ambientes', on_delete=models.CASCADE, null=True, blank=True)
    valor = models.BigIntegerField()
    timestamp = models.DateTimeField()
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
    dados_sensores = models.CharField(max_length=1, choices=DADOS_SENSORES, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    idade = models.PositiveIntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class UploadFileForms(forms.Form):
    file = forms.FileField()