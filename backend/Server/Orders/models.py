from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import MinValueValidator
from Users.models import User
from Carts.models import Cart


class Order(models.Model):
    order_id = ShortUUIDField(
        length=10,
        max_length=10,
        alphabet="1234567890",
        unique=True,
        verbose_name="شناسه سفارش"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='کاربر'
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.PROTECT,
        related_name='order',
        verbose_name='سبد خرید مرتبط'
    )
    total_price = models.PositiveIntegerField(
        verbose_name='مجموع قیمت',
        validators=[MinValueValidator(0)]
    )
    tax = models.PositiveIntegerField(
        verbose_name='مالیات',
        default=0,
        validators=[MinValueValidator(0)]
    )
    discount = models.PositiveIntegerField(
        verbose_name='تخفیف',
        default=0,
        validators=[MinValueValidator(0)]
    )
    final_price = models.PositiveIntegerField(
        verbose_name='قیمت نهایی',
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش {self.order_id} - کاربر {self.user.username}"

    def calculate_prices(self):
        self.total_price = self.cart.total_price
        self.tax = int(self.total_price * 0.1)
        self.discount = self.cart.coupon_discount
        self.final_price = self.total_price + self.tax - self.discount
        return self

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.calculate_prices()
        super().save(*args, **kwargs)

    @property
    def formatted_final_price(self):
        return f"{self.final_price:,} ریال"

    @property
    def formatted_tax(self):
        return f"{self.tax:,} ریال"

    @property
    def formatted_discount(self):
        return f"{self.discount:,} ریال"
