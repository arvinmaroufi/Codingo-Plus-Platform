from django.db import models

from Otps.models import OneTimePassword

from Users.models import User



class UserRegisterOneTimePassword(models.Model):
    otp = models.OneToOneField(
        OneTimePassword,
        on_delete=models.CASCADE,
        related_name="registration_otps"
    )

    username = models.CharField(max_length=40)

    email = models.EmailField()

    phone = models.CharField(max_length=11)

    password = models.CharField(max_length=128)

    full_name = models.CharField(max_length=255)

    password_conf = models.CharField(max_length=255)

    user_type = models.CharField(max_length=3)
    
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Register otp"
        verbose_name_plural = ""

    def __str__(self):
        return f"{self.username} - {self.otp.token} - {self.user_type}"



class UserLoginOneTimePassword(models.Model):

    otp = models.ForeignKey(
        OneTimePassword,
        on_delete=models.CASCADE,
        related_name="login_otps",
        verbose_name="کد یکبار مصرف"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    phone = models.CharField(
        max_length=12,
        verbose_name="شماره تلفن"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )


    class Meta:
        verbose_name = "Login One Time Password"
        verbose_name_plural = "Login One Time Passwords"

    def __str__(self):
        return f"ورود برای {self.user.phone} - {self.otp.token}"