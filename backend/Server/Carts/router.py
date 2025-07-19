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


class CartRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.CartViewSet, basename='cart')

    def get_urls(self):
        return [
            path('', include([
                path('', views.CartViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', views.CartViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
                path('<int:pk>/items/', views.CourseItemViewSet.as_view({
                    'get': 'list',
                    'post': 'create'
                })),
                path('<int:pk>/items/<int:item_pk>/', views.CourseItemViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
            ])),
        ]
    
    
class CourseItemRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseItemViewSet, basename='courseitem')

    def get_urls(self):
        return [
            path('', include([
                path('', views.CourseItemViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<int:pk>/', views.CourseItemViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                })),
            ])),
        ]
