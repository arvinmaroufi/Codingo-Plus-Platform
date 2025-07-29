from django.urls import path, include
from . import routers


app_name = "Profiles"



admin_profile_router = routers.AdminProfileRouter()



urlpatterns = [
    path('admin/', include(admin_profile_router.get_urls())),
]