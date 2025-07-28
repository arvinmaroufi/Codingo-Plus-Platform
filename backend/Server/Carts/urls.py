from django.urls import path, include
from .router import CartRouter, CourseItemRouter


app_name = 'Carts'


cart_router = CartRouter()
course_item_router = CourseItemRouter()

urlpatterns = [
    path('carts/', include(cart_router.get_urls())),
    path('course-items/', include(course_item_router.get_urls())),
]

