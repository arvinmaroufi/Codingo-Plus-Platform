from rest_framework.permissions import BasePermission





class IsProfileOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_staff:
            return True
        
        return False
