from django.urls import path, include
from .router import BlogRouter


app_name = 'Blogs'


blog_router = BlogRouter()

urlpatterns = [
    path('blogs/', include(blog_router.get_urls())),
]
