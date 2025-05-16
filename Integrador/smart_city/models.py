from django.db import models

# Create your models here.

class Sensores:
    sensor = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    unidade_mad = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)

class Ambientes:
    sig = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    ni = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)


class Historico:
    sensor = models.ForeignKey(Sensores, related_name='sensores')
    ambiente = models.ForeignKey(Ambientes, related_name='ambientes')
    observacoes = models.TextField(max_length=300)