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
    

class TicketRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.TicketViewSet, basename='ticket')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.TicketViewSet.as_view({'get': 'list'})),
                path('create/', views.TicketViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.TicketViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls


class TicketMessageRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.TicketMessageViewSet, basename='ticketmessage')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.TicketMessageViewSet.as_view({'get': 'list'})),
                path('create/', views.TicketMessageViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    path('', views.TicketMessageViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls
    
    
class TicketAttachmentRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', views.TicketAttachmentViewSet, basename='ticketattachment')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.TicketAttachmentViewSet.as_view({'get': 'list'})),
                path('create/', views.TicketAttachmentViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    path('', views.TicketAttachmentViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls


class CourseDepartmentRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseDepartmentViewSet, basename='ticket')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CourseDepartmentViewSet.as_view({'get': 'list'})),
                path('create/', views.CourseDepartmentViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.CourseDepartmentViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls
    

class CourseTicketRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseTicketViewSet, basename='ticket')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CourseTicketViewSet.as_view({'get': 'list'})),
                path('create/', views.CourseTicketViewSet.as_view({'post': 'create'})),
                path('<int:pk>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.CourseTicketViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return custom_urls