from rest_framework.permissions import SAFE_METHODS, BasePermission





class IsUserOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_staff:
            return True
        
        return False
    

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True

        if request.user.is_staff:
            return True
        
        return False