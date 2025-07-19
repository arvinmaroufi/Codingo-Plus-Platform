from django.urls import path, include
from .router import CouponRouter, CartRouter


app_name = 'Carts'


coupon_router = CouponRouter()
cart_router = CartRouter()

urlpatterns = [
    path('coupons/', include(coupon_router.get_urls())),
]

