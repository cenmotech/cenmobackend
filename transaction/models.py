import uuid
from django.db import models
from group.models import *
from authuser.models import *

# Create your models here.
class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", null=True)
    date = models.DateTimeField(auto_now_add=True)
    resi = models.CharField(max_length=100, null=True)
    address_user = models.ForeignKey(Address, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    snap_token = models.CharField(max_length=100, null=True)

