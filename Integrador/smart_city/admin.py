from django.contrib import admin
from .models import Historico, Sensores, Ambientes

# Register your models here.

@admin.register(Sensores)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'mac_address', 'unidade_mad', 'valor', 'latitude', 'longitude', 'status', 'timestamp']

@admin.register(Ambientes)
class AmbienteAdmin(admin.ModelAdmin):
    list_display = ['sig', 'descricao', 'ni', 'responsavel']

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'ambiente', 'observacoes']
