from django.urls import path, include

from rest_framework import routers

from . import views





class UserRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.UserViewSet, basename='plans')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.UserViewSet.as_view({'get': 'list'})),
                path('me/', views.UserViewSet.as_view({'get': 'my_user_data'})),
                path('detail/<str:username>/', views.UserViewSet.as_view({'get': 'retrieve'})),
                path('update/<str:username>/', views.UserViewSet.as_view({'put': 'update'})),
            ])),
        ]
        return custom_urls