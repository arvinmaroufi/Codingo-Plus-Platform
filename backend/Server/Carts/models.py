from django.db import models
from django.core.exceptions import ValidationError
from Users.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    class TypeStatusChoices(models.TextChoices):
        EXPIRED = 'EX', 'منقضی شده'
        USED = 'US', 'استفاده شده'
        UNUSED = 'UN', 'استفاده نشده'
    
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد تخفیف'
    )
    discount_value = models.IntegerField(
        verbose_name='مقدار تخفیف (درصد)',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    max_usage = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='حداکثر استفاده'
    )
    usage_count = models.IntegerField(
        default=0,
        verbose_name='تعداد استفاده شده'
    )
    valid_from = models.DateTimeField(
        default=timezone.now,
        verbose_name='معتبر از'
    )
    valid_to = models.DateTimeField(
        verbose_name='معتبر تا'
    )
    type_status = models.CharField(
        max_length=2,
        choices=TypeStatusChoices.choices,
        default=TypeStatusChoices.UNUSED,
        verbose_name='وضعیت کد'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='کاربر اختصاصی',
        help_text='اگر خالی باشد، کد برای همه کاربران معتبر است'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='فعال'
    )

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد ‌های تخفیف'

    def __str__(self):
        return self.code

    def is_valid(self, user=None):
        now = timezone.now()

        if now > self.valid_to:
            self.is_active = False
            self.type_status = self.TypeStatusChoices.EXPIRED
            self.save()
            return False
        
        if self.user and self.user != user:
            return False
        
        if self.max_usage and self.usage_count >= self.max_usage:
            self.is_active = False
            self.type_status = self.TypeStatusChoices.USED
            self.save()
            return False
        
        if not self.is_active:
            return False
        
        return True

    def use(self, user=None):
        is_valid, message = self.is_valid(user)
        if not is_valid:
            raise ValidationError(message)
        
        self.usage_count += 1
        
        if self.max_usage and self.usage_count >= self.max_usage:
            self.is_active = False
            self.type_status = self.TypeStatusChoices.USED
        
        self.save()
        return True
