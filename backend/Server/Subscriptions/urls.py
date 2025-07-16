from django.urls import path, include

from .routers import SubscriptionPlanRouter, SubscriptionRouter





app_name = "Subscriptions"


subscription_plan_router = SubscriptionPlanRouter()
subscription_router = SubscriptionRouter()


urlpatterns = [
    path('plans/', include(subscription_plan_router.get_urls())),
    path('subscriptions/', include(subscription_router.get_urls())),
]