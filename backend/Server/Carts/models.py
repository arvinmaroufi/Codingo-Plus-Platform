from django.db import models
from Users.models import User
from django.utils import timezone
from Courses.models import Course
from Coupons.models import Coupon


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='کاربر'
    )
    coupon = models.ForeignKey(
        Coupon,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='کوپن تخفیف'
    )
    coupon_discount = models.IntegerField(
        default=0,
        verbose_name='مقدار تخفیف اعمال شده'
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
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self):
        return f"سبد خرید {self.user.username}"

    @property
    def total_price(self):
        return sum(item.price for item in self.course_items.all())

    @property
    def final_price(self):
        total = self.total_price
        if self.coupon and self.coupon.is_valid(self.user):
            discount = (total * self.coupon.discount_value) / 100
            return total - discount
        return total


class CourseItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='course_items',
        verbose_name='سبد خرید'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        verbose_name='دوره'
    )
    price = models.PositiveIntegerField(
        verbose_name='قیمت دوره',
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='تاریخ ایجاد'
    )
    
    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم های سبد خرید'
        unique_together = ('cart', 'course')

    def __str__(self):
        return f'{self.course.title} در سبد {self.cart.user.username}'

    def save(self, *args, **kwargs):
        if not self.price or self.price == 0:
            self.price = self.course.price if self.course.price else 0
        super().save(*args, **kwargs)
