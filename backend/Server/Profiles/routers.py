from django.urls import path, include
from rest_framework import routers
from . import views




class AdminProfileRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.AdminProfileViewSet, basename='admins-profiles')

    def get_urls(self):
        return [
            path('', include([
                path('', views.AdminProfileViewSet.as_view({'get': 'list'})),
                path('<str:username>/', views.AdminProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
            ])),
        ]
    

class StudentProfileViewSet(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.StudentProfileViewSet, basename='students-profiles')

    def get_urls(self):
        return [
            path('', include([
                path('', views.StudentProfileViewSet.as_view({'get': 'list'})),
                path('<str:username>/', views.StudentProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
            ])),
        ]


class TheacherProfileViewSet(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.TeacherProfileViewSet, basename='teahcers-profiles')

    def get_urls(self):
        return [
            path('', include([
                path('', views.TeacherProfileViewSet.as_view({'get': 'list'})),
                path('<str:username>/', views.TeacherProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
            ])),
        ]
    