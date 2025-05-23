from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager  # Adjust the path as needed




class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the course platform.

    This model uses a phone number as the primary identifier rather than a username.
    It differentiates between several user types (teacher, student, support, admin)
    and tracks account status.
    """

    class UserTypes(models.TextChoices):
        """
        Choices for specifying the type of user.
        """
        TEACHER = "TE", "آموزگار"      # Instructor
        STUDENT = "ST", "دانش آموز"     # Student
        SUPPORT = "SU", "پشتیبان"       # Support Staff
        ADMIN = "AD", "مدیر"           # Administrator

    class AccountStatus(models.TextChoices):
        """
        Choices for specifying the account status.
        """
        ACTIVE = "ACT", "فعال"         # Account is active
        SUSPENDED = "SUS", "تعلیق شده"    # Account is suspended

    # Field to capture the type of user.
    user_type = models.CharField(
        max_length=2,
        choices=UserTypes.choices,
        verbose_name="نوع کاربر"
    )

    # Field to capture the current status of the account.
    status = models.CharField(
        max_length=3,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
        verbose_name="وضعیت حساب کاربری"
    )

    # User's unique email address.
    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل"
    )

    # Unique phone number used for authentication.
    phone = models.CharField(
        unique=True,
        max_length=11,
        verbose_name="شماره تلفن"
    )

    # Chat-based unique username chosen by the user.
    username = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="نام کاربری"
    )

    # User's full name for display purposes.
    full_name = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name="نام و نام خانوادگی"
    )

    # Automatically set when the user is created.
    joined_date = models.DateField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت"
    )

    # Automatically updated whenever the user record is saved.
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ آخرین به‌روزرسانی"
    )

    # Indicates whether the account is active.
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    # Flag to indicate if the user has administrative rights.
    is_admin = models.BooleanField(
        default=False,
        verbose_name="مدیر"
    )

    # Phone is used as the unique identifier for authentication.
    USERNAME_FIELD = "phone"
    # Required when creating a user via Django's createsuperuser command.
    REQUIRED_FIELDS = ["username", "email", "full_name", "user_type"]

    # Link the custom manager for handling user creation and updates.
    objects = UserManager()

    class Meta:
        ordering = ['joined_date']
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        """
        Return a user-friendly string representation of the user,
        typically the username.
        """
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.
        For simplicity, we check if the user is an admin.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the app `app_label`.
        For simplicity, we return True for admin users.
        """
        return self.is_admin

    @property
    def is_staff(self):
        """
        Return True if the user is considered staff (i.e., an admin).
        """
        return self.is_admin
