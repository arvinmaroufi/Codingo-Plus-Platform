from django.urls import path, include
from .router import MainCategoryRouter


app_name = 'Books'


main_category_router = MainCategoryRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
]
