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
    # ckeditor_editor url
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
