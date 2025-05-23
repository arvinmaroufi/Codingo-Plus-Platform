from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom manager for the User model that handles both regular and
    superuser creation with thorough validation and detailed docstrings.
    """

    def create_user(self, phone, username, email, full_name, user_type, password=None, **extra_fields):
        """
        Create and save a regular user with the given attributes.

        Args:
            phone (str): The user's phone number; used as the unique identifier.
            username (str): The desired username.
            email (str): The user's email address.
            full_name (str): The full name of the user.
            user_type (str): The type of user, as defined in User.UserTypes.
            password (str, optional): The raw user's password.
            **extra_fields: Additional keyword arguments for the user model.

        Returns:
            User: The newly created user instance.

        Raises:
            ValueError: If any of the required fields (phone, username, email, user_type) are not provided.
        """
        if not phone:
            raise ValueError("The Phone field must be set.")
        if not username:
            raise ValueError("The Username field must be set.")
        if not email:
            raise ValueError("The Email field must be set.")
        if not user_type:
            raise ValueError("The User Type must be set.")

        # Normalize the email address by lowercasing the domain part.
        email = self.normalize_email(email)

        # Create the user instance using the provided values.
        user = self.model(
            phone=phone,
            username=username,
            email=email,
            full_name=full_name,
            user_type=user_type,
            **extra_fields
        )

        # Hash the password before saving.
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email, full_name, user_type="AD", password=None, **extra_fields):
        """
        Create and save a superuser with full administrative privileges.

        Args:
            phone (str): The superuser's phone number.
            username (str): The superuser's username.
            email (str): The superuser's email address.
            full_name (str): The full name of the superuser.
            user_type (str): The type of user; defaults to "AD" for admin.
            password (str, optional): The superuser's password.
            **extra_fields: Additional keyword arguments for the user model.

        Returns:
            User: The newly created superuser instance.

        Raises:
            ValueError: If the provided extra fields do not properly designate the user as an admin.
        """
        # Ensure superuser flags are properly set.
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, username, email, full_name, user_type, password, **extra_fields)
