from django.urls import path, include
from .router import BlogRouter, MainCategoryRouter, SubCategoryRouter


app_name = 'Blogs'


blog_router = BlogRouter()
main_category_router = MainCategoryRouter()
sub_category_router = SubCategoryRouter()

urlpatterns = [
    path('blogs/', include(blog_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
]
