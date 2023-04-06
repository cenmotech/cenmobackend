# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    username = None
    is_verif = models.BooleanField(default=False)
    id_photo = models.ImageField(upload_to='id_photo', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_buyerseller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    is_main = models.BooleanField(default=False)



