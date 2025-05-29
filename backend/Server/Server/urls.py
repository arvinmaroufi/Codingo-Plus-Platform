from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('Courses.urls')),
    path('courses/', include('Courses.urls', namespace="Courses")),
    path('profiles/', include('Courses.urls', namespace="Profiles")),
]
