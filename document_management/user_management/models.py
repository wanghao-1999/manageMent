from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # Make username unique
    email = models.EmailField(unique=False)  # Make email non-unique
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
