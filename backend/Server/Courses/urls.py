from django.urls import path, include
from . import routers





main_category_router = routers.MainCategoryRouter()
sub_category_router = routers.SubCategoryRouter()


app_name = 'Courses'
urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
]
