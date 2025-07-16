from django.db import models
from Otps.models import OneTimePassword
from Users.models import User




class AccountResetPassword(models.Model):
    
    otp = models.ForeignKey(
        OneTimePassword,
        on_delete=models.CASCADE,
        related_name="reset_password"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_reset_passwords"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Account reset password"
        verbose_name_plural = "Accounts reset passwords"
        
    
    def __str__(self):
        return f'{self.otp.token}----{self.otp.code}'




class UserCourseEnrollment(models.Model):
    course = models.ForeignKey(
        'Courses.Course',
        on_delete=models.CASCADE,
        related_name="user_activated_course"
    )

    user = models.ForeignKey(
        'Users.User',
        on_delete=models.CASCADE,
        related_name="user_activated_course"
    )

    is_active = models.BooleanField(default=False)

    purchased_on = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User course enrollment"
        verbose_name_plural = "Users courses enrollments"
    
    def __str__(self):
        return f"{self.user.username} puchased the {self.course.title}."
    