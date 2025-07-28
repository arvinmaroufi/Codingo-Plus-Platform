from django.urls import path, include
from rest_framework import routers
from . import views


class OrderRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.OrderViewSet, basename='order')

    def get_urls(self):
        return [
            path('', include([
                path('', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<str:order_id>/', views.OrderViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
                path('my-orders/', views.OrderViewSet.as_view({'get': 'my_orders'})),
            ])),
        ]


class OrderCourseItemRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.OrderCourseItemViewSet, basename='orderitem')

    def get_urls(self):
        return [
            path('', include([
                path('', views.OrderCourseItemViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', views.OrderCourseItemViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
            ])),
        ]
