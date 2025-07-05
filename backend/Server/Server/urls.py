from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('Courses.urls', namespace="Courses")),
    path('profiles/', include('Profiles.urls', namespace="Profiles")),
    path('courses/', include('Courses.urls')),
    path('tickets/', include('Tickets.urls')),
    path('blogs/', include('Blogs.urls')),
    path('auth/', include('Authentication.urls', namespace="authentication")),
    path('articles/', include('Articles.urls')),
    path('books/', include('Books.urls')),
    path('podcasts/', include('Podcasts.urls')),
    # ckeditor_editor url
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
