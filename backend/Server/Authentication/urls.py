from django.urls import path

from . import views



app_name = "authentication"

urlpatterns = [
    path('login-password/', views.LoginPasswordAPIView.as_view(), name="login-password")
]

