from django.urls import path, include
from .router import CouponRouter


app_name = 'Carts'


coupon_router = CouponRouter()

urlpatterns = [
    path('coupons/', include(coupon_router.get_urls())),
]

