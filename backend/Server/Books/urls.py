from django.urls import path, include
from .router import MainCategoryRouter, SubCategoryRouter


app_name = 'Books'


main_category_router = MainCategoryRouter()
sub_category_router = SubCategoryRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
]
