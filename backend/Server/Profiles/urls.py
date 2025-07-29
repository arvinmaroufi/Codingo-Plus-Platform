from django.urls import path, include
from . import routers


app_name = "Profiles"



admin_profile_router = routers.AdminProfileRouter()
student_profile_router = routers.StudentProfileViewSet()
teacher_profile_router = routers.TheacherProfileViewSet()
supporter_profile_router = routers.SupporterProfileViewSet()



urlpatterns = [
    path('admin/', include(admin_profile_router.get_urls())),
    path('student/', include(student_profile_router.get_urls())),
    path('teacher/', include(teacher_profile_router.get_urls())),
    path('supporter/', include(supporter_profile_router.get_urls())),
]