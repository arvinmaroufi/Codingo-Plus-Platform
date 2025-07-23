from django.urls import path, include
from .router import CouponRouter, CartRouter, CourseItemRouter


app_name = 'Carts'


coupon_router = CouponRouter()
cart_router = CartRouter()
course_item_router = CourseItemRouter()

urlpatterns = [
    path('carts/', include(cart_router.get_urls())),
    path('coupons/', include(coupon_router.get_urls())),
    path('course-items/', include(course_item_router.get_urls())),
]

