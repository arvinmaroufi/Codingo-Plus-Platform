from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import User

from Profiles.models import (
    TeacherProfile,
    StudentProfile,
    AdminProfile,
    SupporterProfile,
)

from Subscriptions.models import Subscription, SubscriptionPlan

from Carts.models import Cart
from Wallets.models import Wallet



@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """
    When a new User instance is created:
    Create the appropriate profile based on the user's type:
       - "TE" (Teacher) → TeacherProfile
       - "ST" (Student) → Student
       - "AD" (Admin) → AdminProfile
       - "SU" (Supporter) → SupporterProfile

    A default value ('M') is used for gender here.
    """
    if created:
        # Map user types to their corresponding profile creation,
        # using a default gender ('M'), which you can later update.
        if instance.user_type == User.UserTypes.TEACHER:
            TeacherProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.STUDENT:
            StudentProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.ADMIN:
            AdminProfile.objects.create(user=instance, gender='M')
        elif instance.user_type == User.UserTypes.SUPPORT:
            SupporterProfile.objects.create(user=instance, gender='M')

        now = timezone.now()
        expires_at = now + timezone.timedelta(days=30)

        plan = SubscriptionPlan.objects.get(level=1)

        Subscription.objects.create(
            plan=plan,
            status="AC",
            duration=30,
            user=instance,
            started_at=now,
            expires_at=expires_at,
        )

        Cart.objects.create(user=instance)
        
        Wallet.objects.create(user=instance)