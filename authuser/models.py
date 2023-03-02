from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

