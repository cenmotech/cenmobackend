from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import  status
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from .models import User, Address
from django.contrib.auth.hashers import make_password, check_password
import jwt, datetime
from rest_framework.response import Response
from django.views.decorators.http import require_POST, require_GET
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .decorators import jwt_authenticated



@api_view(['POST'])
def register(request):
    #print csrf token
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        hash_password = make_password(deserialize['password'])
        user = User(name=deserialize['name'], email=deserialize['email'], password=hash_password, phone=deserialize['phone'], is_buyerseller=True)
        #check user already exists on database
        if not (User.objects.filter(email=deserialize['email']).exists()):
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        if User.objects.filter(email=deserialize['email']).exists():
            user = User.objects.get(email=deserialize['email'])
            if check_password(deserialize['password'], user.password):
                user = authenticate(request, email=deserialize['email'], password=deserialize['password'])
                refresh = RefreshToken.for_user(user)
                access = AccessToken.for_user(user)
                access.set_exp(lifetime=datetime.timedelta(days=30))
                refresh.set_exp(lifetime=datetime.timedelta(days=30))
                response = JsonResponse({'refreshToken': str(refresh), 'accessToken': str(access),}, status=status.HTTP_200_OK)
                return response
            else:
                return JsonResponse({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def logout(request):
    #Delete cookie from browser
    if request.method == 'POST':
        response = JsonResponse({'message': 'Logout successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('session_cookie')
        return response
    
@api_view(['GET'])
@jwt_authenticated
def get_user_session(request):
    if request.method == 'GET':
        user = request.user.email
        user = User.objects.get(email=user)
        return JsonResponse({'email': user.email, 'name': user.name, 'phone': user.phone}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def register_admin(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        hash_password = make_password(deserialize['password'])
        user = User(name=deserialize['name'], email=deserialize['email'], password=hash_password, phone=deserialize['phone'], is_admin=True)
        #check user already exists on database
        if not (User.objects.filter(email=deserialize['email']).exists()):
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@jwt_authenticated
def edit_profile(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        user = User.objects.get(email=request.user.email)
        user.name = deserialize['name']
        user.phone = deserialize['phone']
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@jwt_authenticated
def add_address(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        user = User.objects.get(email=request.user.email)
        address = Address(user_id=user, address_name = deserialize['address_name'] ,street=deserialize['street'], city=deserialize['city'], province=deserialize['province'], zip_code=deserialize['zip_code'])
        if not Address.objects.filter(user_id=user).exists():
            address.is_main = True
        address.save()
        return JsonResponse({'message': 'Address added successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_authenticated
def get_user_profile(request):
    if request.method == 'GET':
        user = User.objects.get(email=request.user.email)
        address = Address.objects.filter(user_id=user)
        main_address = Address.objects.get(user_id=user, is_main=True)
        main_address = {'address_name': main_address.address_name, 'street': main_address.street, 'city': main_address.city, 'province': main_address.province, 'zip_code': main_address.zip_code}
        address_list = []
        for i in address:
            address_list.append({'address_name': i.address_name, 'street': i.street, 'city': i.city, 'province': i.province, 'zip_code': i.zip_code, "id": i.id})
        return JsonResponse({'name': user.name, 'email': user.email, 'phone': user.phone, 'address_list': address_list, "address_main": main_address}, status=status.HTTP_200_OK)  

@api_view(['POST'])
@jwt_authenticated
def set_main_address(request, id):
    return None

# @api_view(['GET'])
# @jwt_authenticated
# def testing(request):
#     if request.method == 'GET':
#         user = User.objects.get(email=request.user.email)
#         print(type(user))

    
