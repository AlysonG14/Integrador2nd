from rest_framework.permissions import BasePermission

class IsSensor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'dados_sensores', None) == 'S'

class IsAmbiente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'dados_sensores', None) == 'A'

class IsHistorico(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'dados_sensores', None) == 'H'
    
class IsUsuarioCadastrado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'dados_sensores', None) in ['S', 'A', 'H']