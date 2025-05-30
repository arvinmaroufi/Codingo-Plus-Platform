from django.db import models
from ckeditor.fields import RichTextField



class TeacherProfile(models.Model):

    class GenderChoices(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="provider_profile",
        verbose_name="کاربر"
    )

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        verbose_name="جنسیت"
    )

    age = models.PositiveIntegerField(
        default=18,
        verbose_name="سن"
    )

    bio = RichTextField(
        verbose_name="بیو",
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(
        upload_to='Profiles/teachers/picture/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )

    profile_banner = models.ImageField(
        upload_to='Profiles/teachers/banner/',
        null=True,
        blank=True,
        verbose_name="بنر پروفایل"
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name="در دسترس بودن"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل استاد"
        verbose_name_plural = "پروفایل اساتید"

    def __str__(self):
        return f"{self.user.username} - پروفایل استاد"
