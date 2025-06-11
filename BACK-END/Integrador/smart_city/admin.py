from django.contrib import admin
from .models import Historico, Sensores, Ambientes

# Register your models here.

# Registra a classe Sensores no Admin

@admin.register(Sensores)
class SensorAdmin(admin.ModelAdmin):
    fields = ('sensor', 'mac_address', 'unidade_medida', 'valor', 'latitude', 'longitude', 'status', 'timestamp') # Pega os campos necessários do modelos

# Registra a classe Ambientes no Admin

@admin.register(Ambientes)
class AmbienteAdmin(admin.ModelAdmin):
    fields = ('sig', 'descricao', 'ni', 'responsavel') # Pega os campos necessários do modelos

# Registra a classe Sensores no Admin    

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    fields = ('sensor', 'ambiente', 'observacoes') # Pega os campos necessários do modelos
