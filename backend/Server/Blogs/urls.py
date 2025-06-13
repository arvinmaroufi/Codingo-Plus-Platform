from django.urls import path, include
from .router import BlogRouter, MainCategoryRouter


app_name = 'Blogs'


blog_router = BlogRouter()
main_category_router = MainCategoryRouter()

urlpatterns = [
    path('blogs/', include(blog_router.get_urls())),
    path('main-categories/', include(main_category_router.get_urls())),
]
