from django.urls import path

from . import views



app_name = "authentication"

urlpatterns = [
    path('login-password/', views.LoginPasswordAPIView.as_view(), name="login-password"),

    path('register-request-otp/', views.UserRegisterRequestOtpAPIView.as_view(), name="register-request-otp"),
    path('register-validate-otp/<uuid:token>/', views.UserRegisterValidateOtpAPIView.as_view(), name="register-validate-otp"),

    path('login-request-otp/', views.UserLoginRequestOtpAPIView.as_view(), name="login-request-otp"),
    path('login-validate-otp/', views.UserLoginValidateOtpAPIView.as_view(), name="login-validate-otp"),
]

