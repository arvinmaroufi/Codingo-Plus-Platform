from django.urls import path
from . import views





app_name = "Accounts"



urlpatterns = [
    path('reset-password-request-otp/', views.ResetPasswordRequestOtpAPIView.as_view(), name="reset_password_request_otp"),

    path('reset-password-validate-otp/<str:token>/', views.ResetPasswordValidateOtpAPIView.as_view(), name="reset_password_validate_otp"),
    path('reset-password/', views.AccountResetPasswordAPIView.as_view(), name="reset_password"),
]