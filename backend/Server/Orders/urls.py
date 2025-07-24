from django.urls import path, include
from .router import OrderRouter, OrderCourseItemRouter


app_name = 'Orders'


order_router = OrderRouter()
order_item_router = OrderCourseItemRouter()

urlpatterns = [
    path('orders/', include(order_router.get_urls())),
    path('order-items/', include(order_item_router.get_urls())),
]