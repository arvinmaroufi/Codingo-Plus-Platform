from django.urls import path, include
from .router import DepartmentRouter, TicketRouter


app_name = 'Tickets'


department_router = DepartmentRouter()
ticket_router = TicketRouter()


urlpatterns = [
    path('departments/', include(department_router.get_urls())),
    path('tickets/', include(ticket_router.get_urls())),
]
