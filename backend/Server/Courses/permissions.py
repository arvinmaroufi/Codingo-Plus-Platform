from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True
        

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff
    

class CoursePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            if request.user.type == "TE":
                return True
            return False
        
        return False
    
        
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "DELETE":
            if request.user.is_staff:
                return True
            return False
        
        if request.method == "PUT":
            if request.user.is_staff or request.user == obj.teacher:
                return True
            return False
        
        return False
    


class IsCourseTeacherOrAdmin(BasePermission):

        
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            if request.user.is_staff or request.user.type == "TE":
                return True
            return False
        
        return False
        
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "PUT" or "DELETE":
            if request.user.is_staff or request.user == obj.course.teacher:
                return True
            return False
        
        return False
    
class CourseSessionsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            True
        
        if request.method == "POST":
            if request.user.user_type == 'TE' or request.user.is_staff:
                return True
            return False
        
        return False
    
    
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True
        
        if request.user == obj.chapter.course.teacher:
            return True
        
        return False
    


class CommentsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.mothed in SAFE_METHODS:
            return True
        
        if request.method == 'POST':

            if request.user.is_authenticated:
                return True
            
            return False
        
    
    def has_object_permission(self, request, view, obj):

        if request.mtehod in SAFE_METHODS:
            return True
        
        if request.user.is_staff or request.user == obj.user:
            return True
        
        return False