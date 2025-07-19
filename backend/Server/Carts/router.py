from django.urls import path, include
from rest_framework import routers
from . import views


class CouponRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.CouponViewSet, basename='coupon')

    def get_urls(self):
        return [
            path('', include([
                path('', views.CouponViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', views.CouponViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
            ])),
        ]
