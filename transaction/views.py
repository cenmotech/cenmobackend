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
import base64, os
from dotenv import load_dotenv

load_dotenv()

def create_snap_token(order_id, gross_amount):
    url = os.environ.get('MIDTRANS_URL')+"/snap/v1/transactions"
    server_key = os.environ.get('MIDTRANS_SERVER_KEY')
    payload = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": gross_amount
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic " + base64.b64encode((server_key + ":").encode()).decode()
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
        seller = transaction.seller
        seller.balance += transaction.total_price
        seller.save()
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
        return JsonResponse({'message': 'Transaction success'}, status=status.HTTP_200_OK)
    elif transaction_status == "deny" or status == "cancel":
        transaction.progress = "Failed"
        goods.stock = goods.stock + transaction.quantity
        user = transaction.user
        user.balance += transaction.total_price
        user.save()
        transaction.save()
        goods.save()
        return JsonResponse({'message': 'Transaction failed'}, status=status.HTTP_200_OK)
    elif transaction_status == 'expire':
        transaction.progress = "Expired"
        goods.stock = goods.stock + transaction.quantity
        user = transaction.user
        user.balance += transaction.total_price
        user.save()
        transaction.save()
        goods.save()
        return JsonResponse({'message': 'Transaction expired'}, status=status.HTTP_200_OK)

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
    user = transaction.user
    user.balance += transaction.total_price
    user.save()
    return JsonResponse({'message': 'Transaction Cancelled'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@jwt_authenticated
def finished_transaction(request):
    deserialize = json.loads(request.body)
    transaction = Transaction.objects.get(transaction_id=deserialize)
    transaction.progress = "Completed"
    transaction.save()
    seller = transaction.seller
    seller.balance += transaction.total_price
    seller.save()
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


    
@api_view(['POST'])
@jwt_authenticated
def create_complain(request):
    deserialize = json.loads(request.body)
    user = User.objects.get(email=request.user.email)
    transaction = Transaction.objects.get(transaction_id=deserialize['transactionId'])
    complain = Complain(transaction_id=transaction, user_id=user, complain_text=deserialize['complain_text'], complain_status = "Pending")
    complain.save()
    return JsonResponse({'message': 'Complain created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@jwt_authenticated
def get_complains(request):
    complains = Complain.objects.all().order_by('-date_created')
    complains_list = []
    for complain in complains:
        complain_dict = {}
        complain_dict['complain_id'] = complain.complain_id
        complain_dict['transaction_id'] = str(complain.transaction_id.transaction_id)
        complain_dict['user_id'] = str(complain.user_id.name)
        complain_dict['complain_text'] = complain.complain_text
        complain_dict['complain_status'] = complain.complain_status
        complain_dict['complain_date'] = complain.date_created
        complain_dict['seller_id'] = complain.transaction_id.goods.seller_name
        complain_dict['item_name'] = complain.transaction_id.goods.goods_name
        complain_dict['item_id'] = complain.transaction_id.goods.goods_id

        complains_list.append(complain_dict)

    return JsonResponse({"response":complains_list}, status=status.HTTP_200_OK)

@api_view(['POST'])
@jwt_authenticated
def complain_status(request):
    deserialize = json.loads(request.body)
    complain = Complain.objects.get(complain_id=deserialize['complain_id'])
    if complain.complain_status == "Pending":
        complain.complain_status = "Processing"
        complain.save()
        return JsonResponse({'message': 'Complain updated successfully'}, status=status.HTTP_201_CREATED)
    elif complain.complain_status == "Processing":
        complain.complain_status = "Resolved"
        complain.save()
        return JsonResponse({'message': 'Complain updated successfully'}, status=status.HTTP_201_CREATED)
@jwt_authenticated
@api_view(['GET'])
def get_bank_list(request):
    url = os.environ.get('MIDTRANS_URL')+"/iris/api/v1/beneficiary_banks"
    server_key = os.environ.get('IRIS_SERVER_KEY')
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic " + base64.b64encode((server_key + ":").encode()).decode()
    }
    response = requests.get(url, headers=headers)
    return JsonResponse({"response": response.json()}, status=status.HTTP_200_OK)

@jwt_authenticated
@api_view(['GET'])
def validate_bank(request):
    bank_name = request.GET.get('bank_name')
    bank_no = request.GET.get('bank_no')
    url = f"{os.environ.get('MIDTRANS_URL')}/iris/api/v1/account_validation?bank={bank_name}&account={bank_no}"
    server_key = os.environ.get('IRIS_SERVER_KEY')
    headers = {
        "accept": "application/json",
        "authorization": "Basic " + base64.b64encode((server_key + ":").encode()).decode(),
        "cache-control": "no-cache"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code, response.json())
    if response.status_code == 200:
        return JsonResponse({"response": response.json()}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"response": "Account does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
@jwt_authenticated
@api_view(['POST'])
def add_bank_to_user(request):
    deserialize = json.loads(request.body)
    validation_id = deserialize['validation_id']
    bank_name = deserialize['bank_name']
    account_no = deserialize['account_no']
    account_name = deserialize['account_name']
    user = User.objects.get(email=request.user.email)
    if BankAccount.objects.filter(user=user, account_no=account_no).exists():
        return JsonResponse({"response": "Bank already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        bank = BankAccount.objects.create(id=validation_id, user=user, bank_name=bank_name, account_name=account_name, account_no=account_no)
        bank.save()
        return JsonResponse({"response": "Bank added"}, status=status.HTTP_200_OK)
    
@jwt_authenticated
@api_view(['GET'])
def get_user_bank(request):
    user = User.objects.get(email=request.user.email)
    bank = BankAccount.objects.filter(user=user).values('id', 'bank_name', 'account_name', 'account_no')[::1]
    return JsonResponse({"response": bank}, status=status.HTTP_200_OK)

@jwt_authenticated
@api_view(['GET'])
def get_user_withdrawal(request):
    user = User.objects.get(email=request.user.email)
    withdrawal = WithdrawalHistory.objects.filter(user=user).values('id', 'amount', 'status', 'date')[::1]
    return JsonResponse({"response": withdrawal}, status=status.HTTP_200_OK)

@jwt_authenticated
@api_view(['POST'])
def withdraw(request):
    deserialize = json.loads(request.body)
    bank_id = deserialize['bank_id']
    amount = deserialize['amount']
    user = User.objects.get(email=request.user.email)
    if user.balance < amount:
        amount = user.balance
    bank = BankAccount.objects.get(id=bank_id)
    response = create_payout(bank.account_name, bank.account_no, bank.bank_name, user.email, amount, "Withdraw from ECommerce")
    content = json.loads(response.text)["payouts"][0]
    WithdrawalHistory.objects.create(id=content["reference_no"], user=user, amount=amount, bank_account=bank, status=content["status"])
    user.balance -= amount
    user.save()
    return JsonResponse({"response": "Withdraw request success"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def update_payout_from_midtrans(request):
    deserialize = json.loads(request.body)
    reference_no = deserialize['reference_no']
    status = deserialize['status']
    WithdrawalHistory.objects.filter(id=reference_no).update(status=status)
    return JsonResponse({"response": "Update success"}, status=status.HTTP_200_OK)

def create_payout(account_name, account_number, account_bank, account_email, amount, notes):
    url = os.environ.get('MIDTRANS_URL')+"/iris/api/v1/payouts"
    server_key = os.environ.get('IRIS_SERVER_KEY')
    payload = {
        "payouts": [{
            "beneficiary_name": account_name,
            "beneficiary_account": account_number,
            "beneficiary_bank": account_bank,
            "beneficiary_email": account_email,
            "amount": amount,
            "notes": notes
        }]
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic " + base64.b64encode((server_key + ":").encode()).decode()
    }
    response = requests.post(url, json=payload, headers=headers)
    return response