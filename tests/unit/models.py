"""
Stores models used in unit tests.
"""
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    """
    Custom user model for the unit tests.

    This model is used to demonstrate functionality when the
    primary key and username fields are modified.
    """
    USERNAME_FIELD = 'email'

    my_random_id_field = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
    )
    email = models.EmailField()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.pk
