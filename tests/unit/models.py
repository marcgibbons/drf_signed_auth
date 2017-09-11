from django.contrib.auth.models import AbstractBaseUser


class CustomUser(AbstractBaseUser):
    """
    Custom user model for the unit tests.

    This model is used to demonstrate functionality when the
    primary key and username fields are modified.
    """
    pass
