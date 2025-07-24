from django.urls import path, include
from rest_framework import routers
from . import views


class WalletRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.WalletViewSet, basename='wallet')

    def get_urls(self):
        return [
            path('', include([
                path('', views.WalletViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', views.WalletViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
                path('my-wallet/', views.WalletViewSet.as_view({'get': 'my_wallet'})),
            ])),
        ]
