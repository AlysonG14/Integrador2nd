from rest_framework_simplejwt import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='Home'),
    path('ambiente/criar/', views.createAmbiente, name='Criar Ambiente'),
    path('ambiente/<int:pk>/', views.ambienteDetail, name='Lista de Ambiente'),
    path('historico/criar/', views.createHistorico, name='Criar Histórico'),
    path('historico/<int:pk>/', views.historicoDetail, name='Lista de Históricos'),
    path('sensor/criar/', views.createSensor, name='Criar Sensores'),
    path('sensor/criar/<int:pk>/', views.sensorDetail, name='Lista de Sensores'),
    path('api/token/', TokenObtainPairView, TokenRefreshView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

]