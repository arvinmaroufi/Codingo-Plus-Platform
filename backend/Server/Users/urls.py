from django.urls import path, include

from .routers import UserRouter





app_name = "Users"


user_router = UserRouter()

urlpatterns = [
    path('', include(user_router.get_urls())),
]