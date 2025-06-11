from django.contrib import admin
from django.urls import path
from .  import views
from .views import (CustomTokenObtainPairView, # View para obter token JWT personalizado
CustomTokenRefreshView, # View para atualizaro o token JWT
RegisterView, # View para registrar novo usuário
ProtectedView) # View protegida que requer autenticação JWT

urlpatterns = [

    # Rotas da URLs, utilizando o CRUD: Sensores, Ambientes e Históricos
    
    path('', views.apiOverview, name='Home'), # Rota raíz para visão geral da API 
    path('sensor/', views.SensorList.as_view(), name='Lista de Sensores'), # Rota para listar todos os sensores
    path('sensor/<int:pk>/', views.sensorDetail, name='Detalhes de Sensores'), # Rota para detalhar o histórico
    path('sensor/criar/', views.createSensor, name='Criar Sensores'), # Rota para criar novo sensor
    path('ambiente/', views.AmbienteList.as_view(), name='Lista de Ambiente'), # Rota para listar todos os ambientes
    path('ambiente/<int:pk>/', views.ambienteDetail, name='Detalhes do Ambiente'), # Rota para detalhar o ambiente
    path('ambiente/criar/', views.createAmbiente, name='Criar Ambiente'), # Rota para criar novo ambiente
    path('historico/', views.HistoricoList.as_view(), name='Lista de Históricos'), # Rota para listar todos os históricos
    path('historico/<int:pk>/', views.historicoDetail, name='Detalhes de Históricos'), # Rota para detalhar o histórico
    path('historico/criar/', views.createHistorico, name='Criar Histórico'), # Rota para criar novo histórico

    # URLs somente para o Usuário fazer o cadastramento do sistema

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # Rota para o usuário fazer o cadastro/login no sistema
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), # Rota para pegar o código do 'refresh' após o cadastro ser efetuado
    path('api/token/register/', RegisterView.as_view(), name='register'), # Rota para registrar novo usuário
    path('api/token/protected/', ProtectedView.as_view(), name='protected'), # Rota para ter segurança e protegida

    # URLs para upload de de dados via APIs, utilizando a importação de dados do Excel (.xlsx ou .csv)

    path('api/upload/sensores/', views.upload_sensores_api, name='Importando Dados - Sensores'), # Importando Sensores
    path('api/upload/ambiente/', views.upload_ambiente_api, name='Importando Dados - Ambiente'), # Importando Ambientes
    path('api/upload/historico/', views.upload_historico_api, name='Importando Dados - Histórico') # Importando Históricos
    

]