from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Blog


class IsAdminOrAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True
        
        if request.user.user_type == "TE":
            return True
        

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff or obj.author == request.user