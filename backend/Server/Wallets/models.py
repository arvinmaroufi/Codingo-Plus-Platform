from django.db import models
from Users.models import User


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    value = models.PositiveIntegerField(
        default=0,
        verbose_name='موجودی'
    )

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ ها'

    def __str__(self):
        return f'کیف پول {self.user.username} - موجودی: {self.value}'
    