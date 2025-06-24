from django.urls import include, path
from rest_framework import routers
from . import views

    
    
class DepartmentRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.DepartmentViewSet, basename='ticket')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.DepartmentViewSet.as_view({'get': 'list'})),
                path('create/', views.DepartmentViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.DepartmentViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls
    