from django.urls import path, include

from rest_framework import routers

from . import views


class MainCategoryRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.MainCategoryViewSet, basename='main-categories')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.MainCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),

                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.MainCategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
                ])),
            ])),
        ]
        return custom_urls
    