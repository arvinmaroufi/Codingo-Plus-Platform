from django.urls import include, path
from rest_framework import routers
from . import views


    
class MainCategoryRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.MainCategoryViewSet, basename='article')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.MainCategoryViewSet.as_view({'get': 'list'})),
                path('create/', views.MainCategoryViewSet.as_view({'post': 'create'})),
                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.MainCategoryViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls
    

class SubCategoryRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.SubCategoryViewSet, basename='article')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.SubCategoryViewSet.as_view({'get': 'list'})),
                path('create/', views.SubCategoryViewSet.as_view({'post': 'create'})),
                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.SubCategoryViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls
    

class TagRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.TagViewSet, basename='article')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.TagViewSet.as_view({'get': 'list'})),
                path('create/', views.TagViewSet.as_view({'post': 'create'})),
                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.TagViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls


class AuthorRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.AuthorViewSet, basename='article')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.AuthorViewSet.as_view({'get': 'list'})),
                path('create/', views.AuthorViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    path('', views.AuthorViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls
    


class ArticleRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.ArticleViewSet, basename='article')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.ArticleViewSet.as_view({'get': 'list'})),
                path('create/', views.ArticleViewSet.as_view({'post': 'create'})),
                path('<slug:slug>/', include([
                    path('', views.ArticleViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                    path('publish/', views.ArticleViewSet.as_view({'post': 'publish'})),
                ])),
            ])),
        ]
        return custom_urls



class ArticleContentRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.ArticleContentViewSet, basename='article_content')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.ArticleContentViewSet.as_view({'get': 'list'})),
                path('create/', views.ArticleContentViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    path('', views.ArticleContentViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls