# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from authuser.models import User


class Suggestions(models.Model):
    id_suggestion = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    #Pending, Accepted, Rejected
    status = models.TextField(max_length=20, default="New")