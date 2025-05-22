from rest_framework.permissions import BasePermission

class IsSensor(BasePermission):
    def has_permission(request, self, view):
        return request.user.is_authenticated and getattr(request.user, 'sistema', None) == 'S'

class IsAmbiente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'sistema', None) == 'A'

class IsHistorico(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'sistema', None) == 'H'
    
class IsUsuarioCadastrado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'sistema', None) in ['S', 'A', 'H']