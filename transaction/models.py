import uuid
from django.db import models
from group.models import *
from authuser.models import *
from django.utils import timezone


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

class Complain(models.Model):
    complain_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    complain_text = models.TextField(max_length=400)
    complain_status = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    
class BankAccount(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=50)

class WithdrawalHistory(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

