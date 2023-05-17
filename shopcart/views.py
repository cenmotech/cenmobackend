from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
import json
from .models import Cart, CartItem
from authuser.models import User
from group.models import Goods
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from authuser.decorators import jwt_authenticated
# Create your views here.

@api_view(['POST'])
@jwt_authenticated
def update_to_cart(request):
    user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        action = deserialize['action']

        cart, created = Cart.objects.get_or_create(user=user)
        goods_object = Goods.objects.get(goods_id=deserialize['goods_id'])
        cartItem, created = CartItem.objects.get_or_create(
            goods= goods_object,
            cart=cart)
        
        if action == 'add' and cartItem.quantity < goods_object.stock :
            cartItem.quantity = (cartItem.quantity + 1)
        elif action == 'remove':
            cartItem.quantity = (cartItem.quantity - 1)
        elif action == 'delete':
            cartItem.quantity = 0
        elif action == 'change':
            cartItem.quantity = deserialize['amount']

        cartItem.save()

        if cartItem.quantity <= 0:
            cartItem.delete()
        return JsonResponse({'message': 'Item updated to cart successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_cart(request):
    user = User.objects.get(email=request.user.email)
    if request.method == 'GET':
        cart = Cart.objects.get(user=user)
        cartItems = cart.cartitems.all()
        items = cartItems.values("goods__goods_id", "goods__goods_name", "goods__goods_description", "goods__goods_image_link","goods__goods_price", "goods__seller_name","goods__stock","quantity", "id")
        return JsonResponse({"response": list(items)}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_carts_item(request, items_id):
    print("test")
    user = User.objects.get(email=request.user.email)
    if request.method == 'GET':
        cart = Cart.objects.get(user=user)
        cartItem = cart.cartitems.filter(id = items_id).values()[0]
        return JsonResponse({"response": cartItem}, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_total_price(request):
    user = User.objects.get(email=request.user.email)
    if request.method == 'GET':
        cart = Cart.objects.get(user=user)
        
        cartItems = cart.cartitems.all()
        items = cartItems.values("goods__goods_id", "goods__goods_name", "goods__goods_description", "goods__goods_image_link","goods__goods_price", "goods__seller_name","quantity")
        itemDupe = items
        total = 0
        for itemprice in itemDupe:
            total += itemprice["goods__goods_price"] * itemprice["quantity"]
        return JsonResponse({"total":total}, safe=False, status=status.HTTP_200_OK)