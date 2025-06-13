from django.db import models
from django.utils import timezone

import uuid



class OneTimePassword(models.Model):
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP' 
        ACTIVE = 'ACT'
        USED = 'USE'

    status = models.CharField(
        max_length=3,
        choices=OtpStatus.choices,
        default=OtpStatus.ACTIVE
    )
    
    token = models.UUIDField(verbose_name="توکن", primary_key=True, default=uuid.uuid4)
    
    code = models.CharField(max_length=6)
    
    expiration = models.DateTimeField(blank=True, null=True)

    is_used = models.BooleanField(default=False, verbose_name="استفاده شده؟")
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    class Meta:
        verbose_name = "رمز یکبار مصرف"
        verbose_name_plural = "رمز های یکبار مصرف"

    def __str__(self):
        return f'{self.status}----{self.code}----{self.token}'

    def get_expiration(self):
        expiration = self.created_at + timezone.timedelta(minutes=2)
        self.expiration = expiration
        self.save()

    def status_validation(self):
        if self.is_used == True:
            self.status = 'USE'
        if self.expiration <= timezone.now():
            if not self.status == 'USE':
                self.status = 'EXP'
                return self.status
            else:
                return self.status
        else:
            return self.status