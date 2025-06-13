from django.db import models

from Otps.models import OneTimePassword




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
