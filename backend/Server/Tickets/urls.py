from django.urls import path, include
from .router import DepartmentRouter, TicketRouter, TicketMessageRouter


app_name = 'Tickets'


department_router = DepartmentRouter()
ticket_router = TicketRouter()
ticket_message_router = TicketMessageRouter()


urlpatterns = [
    path('departments/', include(department_router.get_urls())),
    path('tickets/', include(ticket_router.get_urls())),
    path('ticket-messages/', include(ticket_message_router.get_urls())),
]
