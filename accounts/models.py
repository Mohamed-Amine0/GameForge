from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    # Add additional fields if needed
    api_usage_count = models.IntegerField(default=0, help_text=_("Number of API calls made by the user"))

    def __str__(self):
        return self.username
