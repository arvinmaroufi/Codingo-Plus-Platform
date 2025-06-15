from rest_framework.permissions import BasePermission



class IsNotAuthenticated(BasePermission):
    
    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return False
        
        return True