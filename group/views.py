from django.http import response, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Group, Goods, Post, Category
from authuser.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import status
from django.views.decorators.http import require_POST, require_GET
from authuser.decorators import jwt_authenticated
from rest_framework.decorators import api_view
import json, jwt
from django.views.decorators.http import require_POST, require_GET

@api_view(['POST'])
@jwt_authenticated
def create_group(request):
    user = User.objects.get(email=request.user.email)
    if user and user.is_admin:
        deserialize = json.loads(request.body)
        category = Category.objects.get(category_id=deserialize['category'])
        group = Group(group_name=deserialize['name'], group_desc=deserialize['desc'], group_photo_profile_link=deserialize['photo_profile'], group_category=category)
        if not (Group.objects.filter(group_name=deserialize['name']).exists()):
            group.save()
            return JsonResponse({'message': 'Group created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message': 'Group already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@jwt_authenticated
def create_category(request):
    user = User.objects.get(email=request.user.email)
    if user and user.is_admin:
            deserialize = json.loads(request.body)
            category = Category(category_name=deserialize['name'])
            if not (Category.objects.filter(category_name=deserialize['name']).exists()):
                category.save()
                return JsonResponse({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'message': 'Category already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@jwt_authenticated
def join_group(request):
    user = User.objects.get(email=request.user.email)
    deserialize = json.loads(request.body)
    group = Group.objects.get(group_id=deserialize['id'])
    if not (group.group_member.filter(email=user.email).exists()):
        print(group.group_member)
        group.group_member.add(user)
        return JsonResponse({'message': 'Group Joined'}, status=status.HTTP_200_OK)
    else:
        print(group.group_member)
        return JsonResponse({'message': 'Group already exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@jwt_authenticated
def is_joined(request, group_id):
    result = Group.objects.filter(group_id=group_id, group_member = request.user.email)
    if len(result) == 0:
        is_member = False
    else:
        is_member = True
    return JsonResponse({"isMember":is_member}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated     
def search_group(request, name):
    group = Group.objects.filter(group_name__icontains=name).values()[::1]
    return JsonResponse({"response":group}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated   
def see_group(request, group_id):
    group = Group.objects.filter(group_id=group_id).values()[0]
    return JsonResponse({"response":group}, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_all_categories_contains(request, keyword):
    group = Group.objects.filter(group_name__icontains=keyword)
    category_groups = {}
    for category in group:
        category_name = category.group_category.category_name
        if category_name not in category_groups:
            category_groups[category_name] = []
            category_groups[category_name].append({"group_name": category.group_name,
                    "group_id": category.group_id})
        else :
            category_groups[category_name].append({"group_name": category.group_name,
            "group_id": category.group_id})
    return JsonResponse({'category_groups': category_groups}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_all_categories(request):
    group = Group.objects.all()
    category_groups = {}
    for category in group:
        category_name = category.group_category.category_name
        if category_name not in category_groups:
            category_groups[category_name] = []
            category_groups[category_name].append({"group_name": category.group_name,
                    "group_id": category.group_id})
        else :
            category_groups[category_name].append({"group_name": category.group_name,
            "group_id": category.group_id})
    return JsonResponse({'category_groups': category_groups}, safe=False, status=status.HTTP_200_OK)
            
@api_view(['POST'])
@jwt_authenticated 
def create_post(request):
    user = User.objects.get(email=request.user.email)
    deserialize = json.loads(request.body)
    group = Group.objects.get(group_id=deserialize['group'])
    post = Post(post_desc=deserialize['desc'],post_image_link=deserialize['image'], post_group_origin=group, post_user=user)
    post.save()
    return JsonResponse({"message": "Post created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@jwt_authenticated
def create_listing(request):
    user = User.objects.get(email=request.user.email)
    deserialize = json.loads(request.body)
    group = Group.objects.get(group_id=deserialize['group'])
    goods = Goods(goods_name=deserialize['name'], goods_price=deserialize['price'], goods_description=deserialize['desc'], goods_image_link=deserialize['image'], goods_region=deserialize['region'], goods_group_origin=group, goods_seller=user)
    goods.save()
    return JsonResponse({"message": "Listing created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@jwt_authenticated
def search_post_by_desc(request, desc):
    post = Post.objects.filter(post_desc__icontains=desc).values()[::1]
    return JsonResponse({"response":post}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def search_post_on_group(request, desc, group):
    group = Group.objects.get(group_id=group)
    post = Post.objects.filter(post_group_origin=group, post_desc__icontains=desc).order_by('-post_id').values()[::1]
    return JsonResponse({"response":post}, safe=False, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@jwt_authenticated
def get_post_by_logged_user(request):
    user = User.objects.get(email=request.user.email)
    post = Post.objects.filter(post_user=user).order_by('-post_id').values()[::1]
    return JsonResponse({"response":post}, safe=False, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@jwt_authenticated
def get_post_on_group(request, group):
    group = Group.objects.get(group_id=group)
    post = Post.objects.filter(post_group_origin=group).order_by('-post_id').values()[::1]
    return JsonResponse({"response":post}, safe=False, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@jwt_authenticated
def search_listing_by_name(request, name):
    goods = Goods.objects.filter(goods_name__icontains=name).order_by('-goods_id').values()[::1]
    return JsonResponse({"response":goods}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def search_listing_on_group(request, name, group):
    group = Group.objects.get(group_id=group)
    goods = Goods.objects.filter(goods_group_origin=group, goods_name__icontains=name).order_by('-goods_id').values()[::1]
    return JsonResponse({"response":goods}, safe=False, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@jwt_authenticated
def get_listing_by_logged_user(request):
    user = User.objects.get(email=request.user.email)
    goods = Goods.objects.filter(goods_seller=user).order_by('-goods_id').values()[::1]
    return JsonResponse({"response":goods}, safe=False, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@jwt_authenticated
def get_listing_by_seller(request, email):
    user = User.objects.get(email=request.user.email)
    goods = Goods.objects.filter(goods_seller=user).order_by('-goods_id').values()[::1]
    return JsonResponse({"response":goods}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])  
@jwt_authenticated
def get_listing_by_seller_on_group(request, group, email):
    user = User.objects.get(email=email)
    group = Group.objects.get(group_id=group)
    goods = Goods.objects.filter(goods_group_origin=group, goods_seller=user).order_by('-goods_id').values()[::1]
    return JsonResponse({"response":goods}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def get_listing_on_group(request, group):
    group = Group.objects.get(group_id=group)
    goods = Goods.objects.filter(goods_group_origin=group).order_by('-goods_id').values()[::1]
    return JsonResponse({"response":goods}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_authenticated
def delete_post(request, postingan_id, group):
    user = User.objects.get(email=request.user.email)
    post = Post.objects.get(post_id=postingan_id, post_group_origin=group)
    if post.post_user == user or user.is_admin:
        post.delete()
        return JsonResponse({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    