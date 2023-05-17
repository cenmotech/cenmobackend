from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from authuser.decorators import jwt_authenticated
from group.models import *
from shopcart.models import Cart
from .models import *
from authuser.models import *
from django.http import HttpRequest, response, HttpResponse, JsonResponse
from rest_framework import status
import requests, json

def create_snap_token(order_id, gross_amount):
    url = "https://app.sandbox.midtrans.com/snap/v1/transactions"
    payload = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic U0ItTWlkLXNlcnZlci01NGNNWmRraGo5N0JEa256X3hvV0htZk06"
    }

    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)["token"]

@api_view(['POST'])
@jwt_authenticated
def make_transaction(request):
    deserialize = json.loads(request.body)
    goods = Goods.objects.get(goods_id=deserialize['goodId'])
    user = User.objects.get(email=request.user.email)
    #Check address if not exist in Address table search by email and is_main
    if Address.objects.filter(user=user, is_main=True).exists():
        deserialize = json.loads(request.body)
        goods = Goods.objects.get(goods_id=deserialize['goodId'])
        user = User.objects.get(email=request.user.email)
        address = Address.objects.get(user_id = request.user.email, is_main=True)
        quantity = deserialize['quantity']
        price = goods.goods_price
        total_price = int(quantity) * int(price)
        transaction_id=uuid.uuid4()

        goods.stock = int(goods.stock) - int(quantity)
        goods.save()

        cart = Cart.objects.get(user=user)
        cartItem = cart.cartitems.get(goods = goods)
        cartItem.delete()

        snap_token = create_snap_token(str(transaction_id), total_price)
        transactions = Transaction(user_id=user, seller=goods.goods_seller ,price=price, total_price=total_price, address_user_id=address.id,goods_id=goods.goods_id, transaction_id=transaction_id, quantity=quantity,progress="Pending", snap_token=snap_token)
        transactions.save()
        return JsonResponse({'message': 'Transaction made successfully', 'token': snap_token}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@jwt_authenticated
def update_transaction(request):
    deserialize = json.loads(request.body)
    transaction = Transaction.objects.get(transaction_id=deserialize['transactionId'])
    print(transaction)
    if transaction.progress == "Verifying":
        transaction.progress = "Processing"
        transaction.resi = deserialize['resi']
        print('didalam if')
        transaction.save()
        return JsonResponse({'message': 'Transaction updated successfully'}, status=status.HTTP_201_CREATED)
    else:
        transaction.progress = "Completed"
        transaction.save()
        return JsonResponse({'message': 'Transaction updated successfully'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def get_update_from_midtrans(request):
    deserialize = json.loads(request.body)
    transaction = Transaction.objects.get(transaction_id=deserialize['order_id'])
    goods = Goods.objects.get(goods_id=transaction.goods_id)
    transaction_status = deserialize["transaction_status"]
    if transaction_status == "settlement" or status == "capture":
        transaction.progress = "Verifying"
        transaction.save()
        return JsonResponse({'message': 'Transaction success'}, status=status.HTTP_201_CREATED)
    elif transaction_status == "deny" or status == "cancel":
        transaction.progress = "Failed"
        goods.stock = goods.stock + transaction.quantity
        transaction.save()
        goods.save()
        return JsonResponse({'message': 'Transaction failed'}, status=status.HTTP_201_CREATED)
    elif transaction_status == 'expired':
        transaction.progress = "Expired"
        goods.stock = goods.stock + transaction.quantity
        transaction.save()
        goods.save()
        return JsonResponse({'message': 'Transaction expired'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@jwt_authenticated
def get_seller_transaction(request):
    transactions = Transaction.objects.filter(seller_id=request.user.email)
    transaction_list = []
    for transaction in transactions:
        transaction_list.append({
            "transactionId": transaction.transaction_id,
            "date": transaction.date,
            "goodsName": transaction.goods.goods_name,
            "quantity": transaction.quantity,
            "price": transaction.price,
            "totalPrice": transaction.total_price,
            "progress": transaction.progress,
            "resi": transaction.resi,
            "snapToken": transaction.snap_token,
            "buyer_name": User.objects.get(email=transaction.user_id).name,
            "buyer_name": User.objects.get(email=transaction.user_id).name
        })
    return JsonResponse({'transactions': transaction_list}, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_buyer_by_goods_id(request, goods_id):
        transactions = Transaction.objects.filter(seller_id=request.user.email, goods_id=goods_id)
        transaction_list = []
        for transaction in transactions:
                transaction_list.append({
                "goodsId" : transaction.goods.goods_id,
                "transactionId": transaction.transaction_id,
                "date": transaction.date,
                "goodsName": transaction.goods.goods_name,
                "quantity": transaction.quantity,
                "price": transaction.price,
                "totalPrice": transaction.total_price,
                "progress": transaction.progress,
                "resi": transaction.resi,
                "snapToken": transaction.snap_token,
                "buyer_name": User.objects.get(email=transaction.user_id).name
            })
        return JsonResponse({'transactions': transaction_list}, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_authenticated
def cancel_transaction(request):
    deserialize = json.loads(request.body)
    transaction = Transaction.objects.get(transaction_id=deserialize)
    transaction.progress = "Cancelled"
    transaction.save()
    return JsonResponse({'message': 'Transaction Cancelled'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@jwt_authenticated
def finished_transaction(request):
    deserialize = json.loads(request.body)
    transaction = Transaction.objects.get(transaction_id=deserialize)
    transaction.progress = "Completed"
    transaction.save()
    return JsonResponse({'message': 'Transaction Finished'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@jwt_authenticated
def get_user_transaction(request):
    get_user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.filter(user=get_user).order_by('-date').values('goods__goods_name', 'goods__seller_name','goods__goods_image_link','goods__goods_description',
        'transaction_id','date','resi','address_user','progress','quantity','price','total_price','snap_token')[::1]
    return JsonResponse({"response": transaction}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_user_pending_transaction(request):
    get_user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.filter(user=get_user,progress="Pending").order_by('-date').values('goods__goods_name', 'goods__seller_name','goods__goods_image_link','goods__goods_description',
        'transaction_id','date','resi','address_user','progress','quantity','price','total_price','snap_token')[::1]
    return JsonResponse({"response": transaction}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_user_verifying_transaction(request):
    get_user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.filter(user=get_user,progress="Verifying").order_by('-date').values('goods__goods_name', 'goods__seller_name','goods__goods_image_link','goods__goods_description',
        'transaction_id','date','resi','address_user','progress','quantity','price','total_price','snap_token')[::1]
    return JsonResponse({"response": transaction}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_user_processing_transaction(request):
    get_user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.filter(user=get_user,progress="Processing").order_by('-date').values('goods__goods_name', 'goods__seller_name','goods__goods_image_link','goods__goods_description',
        'transaction_id','date','resi','address_user','progress','quantity','price','total_price','snap_token')[::1]
    return JsonResponse({"response": transaction}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_user_completed_transaction(request):
    get_user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.filter(user=get_user,progress="Completed").order_by('-date').values('goods__goods_name', 'goods__seller_name','goods__goods_image_link','goods__goods_description',
        'transaction_id','date','resi','address_user','progress','quantity','price','total_price','snap_token')[::1]
    return JsonResponse({"response": transaction}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_user_cancelled_transaction(request):
    get_user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.filter(user=get_user,progress="Cancelled").order_by('-date').values('goods__goods_name', 'goods__seller_name','goods__goods_image_link','goods__goods_description',
        'transaction_id','date','resi','address_user','progress','quantity','price','total_price','snap_token')[::1]
    return JsonResponse({"response": transaction}, safe=False, status=status.HTTP_200_OK)

