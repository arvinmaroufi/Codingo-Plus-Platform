from django.urls import path, include
from .router import DepartmentRouter, TicketRouter, TicketMessageRouter, TicketAttachmentRouter, CourseDepartmentRouter, CourseTicketRouter


app_name = 'Tickets'


department_router = DepartmentRouter()
ticket_router = TicketRouter()
ticket_message_router = TicketMessageRouter()
ticket_attachment_router = TicketAttachmentRouter()
course_department_router = CourseDepartmentRouter()
course_ticket_router = CourseTicketRouter()


urlpatterns = [
    path('departments/', include(department_router.get_urls())),
    path('tickets/', include(ticket_router.get_urls())),
    path('ticket-messages/', include(ticket_message_router.get_urls())),
    path('ticket-attachments/', include(ticket_attachment_router.get_urls())),
    path('course_departments/', include(course_department_router.get_urls())),
    path('course_tickets/', include(course_ticket_router.get_urls())),
]
