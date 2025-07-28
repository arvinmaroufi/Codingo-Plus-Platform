from rest_framework.permissions import BasePermission


class IsCouponOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user if obj.user else False
