from django.urls import include, path
from rest_framework import routers
from . import views


    
class MainCategoryRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.MainCategoryViewSet, basename='podcast')

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
        self.register(r'', views.SubCategoryViewSet, basename='podcast')

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
        self.register(r'', views.TagViewSet, basename='podcast')

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


class PodcastRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.PodcastViewSet, basename='podcast')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.PodcastViewSet.as_view({'get': 'list'})),
                path('create/', views.PodcastViewSet.as_view({'post': 'create'})),
                path('<slug:slug>/', include([
                    path('', views.PodcastViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                    path('contents/', include([
                        path('', views.PodcastContentViewSet.as_view({'get': 'list'})),
                        path('create/', views.PodcastContentViewSet.as_view({'post': 'create'})),
                        path('<int:pk>/', views.PodcastContentViewSet.as_view({
                            'get': 'retrieve',
                            'put': 'update',
                            'delete': 'destroy'
                        })),
                    ])),
                ])),
            ])),
        ]
        return custom_urls


class CommentReplyRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.CommentReplyViewSet, basename='podcast')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CommentReplyViewSet.as_view({'get': 'list'})),
                path('create/', views.CommentReplyViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', views.CommentReplyViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'delete': 'destroy'
                })),
            ])),
        ]
        return custom_urls


class CommentRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.CommentViewSet, basename='podcast')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CommentViewSet.as_view({'get': 'list'})),
                path('create/', views.CommentViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    path('', views.CommentViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                    path('replies/', views.CommentReplyViewSet.as_view({'get': 'list'})),
                ])),
            ])),
        ]
        return custom_urls
