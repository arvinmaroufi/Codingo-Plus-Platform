from django.urls import path, include
from . import routers



app_name = "Courses"


main_category_router = routers.MainCategoryRouter()
sub_category_router = routers.SubCategoryRouter()
tags_router = routers.SubCategoryRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tags_router.get_urls())),
]
