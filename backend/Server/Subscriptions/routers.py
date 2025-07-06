from django.urls import path, include

from rest_framework import routers

from . import views


class SubscriptionPlanRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.SubscriptionPlanViewSet, basename='plans')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.SubscriptionPlanViewSet.as_view({'get': 'list', 'post': 'create'})),
                path('<slug:slug>/', views.SubscriptionPlanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
            ])),
        ]
        return custom_urls
    

class SubscriptionRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.SubscriptionViewSet, basename='subscription')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.SubscriptionViewSet.as_view({'get': 'list'})),
                path('<slug:slug>/', views.SubscriptionViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                path('my-subscription/', views.SubscriptionViewSet.as_view({'get': 'my_subscription'})),
            ])),
        ]
        return custom_urls