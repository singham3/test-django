from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=13, null=True, blank=True, unique=True)
    is_mobile = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'mobile', 'is_mobile', 'is_email', 'updated_at']

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile

    class Meta:
        verbose_name_plural = "User"
