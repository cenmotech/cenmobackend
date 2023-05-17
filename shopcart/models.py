from django.db import models
from authuser.models import User
from group.models import Goods

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', null=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=0, null=True, blank=True)