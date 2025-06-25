from django.urls import path, include
from .router import DepartmentRouter


app_name = 'Tickets'


department_router = DepartmentRouter()


urlpatterns = [
    path('departments/', include(department_router.get_urls())),
]
