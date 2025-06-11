from django.contrib import admin
from django.urls import path
from .  import views
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, RegisterView, ProtectedView

urlpatterns = [
    path('', views.apiOverview, name='Home'),
    path('ambiente/criar/', views.createAmbiente, name='Criar Ambiente'),
    path('ambiente/', views.AmbienteList.as_view(), name='Lista de Ambiente'),
    path('ambiente/<int:pk>/', views.ambienteDetail, name='Detalhes do Ambiente'),
    path('historico/criar/', views.createHistorico, name='Criar Histórico'),
    path('historico/', views.HistoricoList.as_view(), name='Lista de Históricos'),
    path('historico/<int:pk>/', views.historicoDetail, name='Detalhes de Históricos'),
    path('sensor/criar/', views.createSensor, name='Criar Sensores'),
    path('sensor/', views.SensorList.as_view(), name='Lista de Sensores'),
    path('sensor/criar/<int:pk>/', views.sensorDetail, name='Detalhes de Sensores'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/register/', RegisterView.as_view(), name='register'),
    path('api/token/protected/', ProtectedView.as_view(), name='protected'),
    path('api/upload/sensores/', views.upload_sensores_api, name='Importando Dados - Sensores'),
    path('api/upload/ambiente/', views.upload_ambiente_api, name='Importando Dados - Ambiente'),
    path('api/upload/historico/', views.upload_historico_api, name='Importando Dados - Histórico')
    

]