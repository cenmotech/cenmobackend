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



@api_view(['GET'])
@jwt_authenticated
def get_suggestions(request):
    #Check if user is admin
    if request.user.is_admin:
        suggestions = Suggestions.objects.all().order_by('-date')
        suggestions_list = []
        for suggestion in suggestions:
            suggestion_dict = {}
            suggestion_dict['id'] = suggestion.id_suggestion
            suggestion_dict['suggestion'] = suggestion.suggestion
            suggestion_dict['date'] = suggestion.date
            suggestion_dict['status'] = suggestion.status
            suggestion_dict['user'] = suggestion.user_id
            suggestion_dict['name'] = User.objects.get(email=suggestion.user_id).name
            suggestions_list.append(suggestion_dict)
        #Sort based on the date
        return JsonResponse({'suggestions_list': suggestions_list}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'User is not admin'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@jwt_authenticated
def change_status_suggestions(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        suggestion = Suggestions.objects.get(id_suggestion=deserialize['id'])
        suggestion.status = "Seen"
        suggestion.save()
        return JsonResponse({'message': 'Status changed successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@jwt_authenticated
def add_suggestion(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        suggestion = Suggestions(user=request.user, suggestion=deserialize['suggestion'])
        suggestion.save()
        return JsonResponse({'message': 'Suggestion added successfully'}, status=status.HTTP_200_OK)  

@api_view(['GET'])
@jwt_authenticated
def get_all_groups_data(request):
    if request.method == 'GET':
        groups = Group.objects.all().order_by('group_name')
        groups_list = []
        for group in groups:
            group_dict = {}
            group_dict['group_id'] = group.group_id
            group_dict['group_name'] = group.group_name
            group_dict['group_desc'] = group.group_desc
            group_dict['group_photo_profile_link'] = group.group_photo_profile_link
            group_dict['group_total_member'] = group.group_total_member
            group_dict['date_created'] = group.date_created
            group_dict['group_category'] = group.group_category.category_name
            groups_list.append(group_dict)
        return JsonResponse({'groups_list': groups_list}, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@jwt_authenticated
def get_all_categories_for_admin(request):
    category = Category.objects.all()
    category_groups = []
    for cat in category:
        category_groups.append({"category_name": cat.category_name,
                                "category_id": cat.category_id})
    return JsonResponse({'category_groups': category_groups}, safe=False, status=status.HTTP_200_OK)
