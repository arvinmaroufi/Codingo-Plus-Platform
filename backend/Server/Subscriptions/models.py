from django.db import models
from django.utils import timezone




class SubscriptionPlan(models.Model):
    
    name = models.CharField(max_length=210, unique=True)
    slug = models.SlugField(max_length=210, unique=True, primary_key=True)

    description = models.TextField()

    level = models.IntegerField(default=1)

    price_per_day = models.IntegerField(default=0)
    

    class Meta:
        verbose_name = "Subscription plan"
        verbose_name_plural = "Subscription plans"

    
    def __str__(self):
        return self.name
    


class Subscription(models.Model):

    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'AC', 'فعال'
        INACTIVE = 'IN', 'غیر فعال'

    user  = models.OneToOneField(
        "Users.User",
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="user_subscription"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.DO_NOTHING,
        related_name="plans_subscriptions"
    )

    status = models.CharField(
        max_length=2,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.INACTIVE,
    )

    duration = models.IntegerField(default=0)

    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ('user','plan')


    def __str__(self):
        return f"{self.user} → {self.plan} ({self.status})"
    

    def is_active(self):
        now = timezone.now()
        if self.expires_at <= now:
            if self.status == self.SubscriptionStatus.ACTIVE:
                self.status = self.SubscriptionStatus.INACTIVE
                self.save()
                return False
            return False
        return True
