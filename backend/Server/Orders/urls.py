from django.urls import path, include
from .router import OrderRouter


app_name = 'Orders'


order_router = OrderRouter()

urlpatterns = [
    path('orders/', include(order_router.get_urls())),

]