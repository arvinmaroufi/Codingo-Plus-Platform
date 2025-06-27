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
    

class SubCategoryRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.SubCategoryViewSet, basename='sub-categories')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.SubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),

                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.SubCategoryViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
                ])),
            ])),
        ]
        return custom_urls
    

class TagRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.TagViewSet, basename='tags')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.TagViewSet.as_view({'get': 'list', 'post': 'create'})),

                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.TagViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
                ])),
            ])),
        ]
        return custom_urls
    


class CourseRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseViewSet, basename='courses')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CourseViewSet.as_view({'get': 'list', 'post': 'create'})),

                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT, DELETE.
                    path('', views.CourseViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
                ])),
            ])),
        ]
        return custom_urls
    


class CourseFaqRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseFaqViewSet, basename='course-faqs')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CourseFaqViewSet.as_view({'get': 'list'})),

                path('course-faqs/<slug:slug>/', views.CourseFaqViewSet.as_view({'get': 'course_faqs'})),

                path('create/', views.CourseFaqViewSet.as_view({'post': 'create'})),
                path('detail/<int:pk>/', views.CourseFaqViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', views.CourseFaqViewSet.as_view({'put': 'update'})),
                path('delete/<int:pk>/', views.CourseFaqViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls
    


class CourseContentRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseContentViewSet, basename='course-contents')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CourseContentViewSet.as_view({'get': 'list'})),

                path('course-contents/<slug:slug>/', views.CourseContentViewSet.as_view({'get': 'course_contents'})),

                path('create/', views.CourseContentViewSet.as_view({'post': 'create'})),
                path('detail/<int:pk>/', views.CourseContentViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', views.CourseContentViewSet.as_view({'put': 'update'})),
                path('delete/<int:pk>/', views.CourseContentViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls



class CourseChapterRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.register(r'', views.CourseChapterViewSet, basename='course-chapters')

    def get_urls(self):
        custom_urls = [
            path('', include([
                path('', views.CourseChapterViewSet.as_view({'get': 'list'})),

                path('course-chapters/<slug:slug>/', views.CourseChapterViewSet.as_view({'get': 'course_chapters'})),

                path('create/', views.CourseChapterViewSet.as_view({'post': 'create'})),
                path('detail/<int:pk>/', views.CourseChapterViewSet.as_view({'get': 'retrieve'})),
                path('update/<int:pk>/', views.CourseChapterViewSet.as_view({'put': 'update'})),
                path('delete/<int:pk>/', views.CourseChapterViewSet.as_view({'delete': 'destroy'})),
            ])),
        ]
        return custom_urls
    