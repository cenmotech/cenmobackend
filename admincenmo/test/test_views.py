import datetime
from django.http import HttpResponse
from django.urls import reverse, resolve
from django.test import Client, TestCase, RequestFactory
from django.test import SimpleTestCase, TestCase, RequestFactory
import jwt
from rest_framework import  status
from admincenmo.views import *
from django.contrib.auth.hashers import make_password
import json
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from cenmobackend import settings
from group.models import *

class TestViews(TestCase):
    def setUp(self):
        self.admin = User(name="meh",email="testing@gmail.com", password=make_password("asd123"),phone="1234567890")
        self.admin.is_admin = True
        self.admin.save()
        self.user = User(name="meh",email="meh@gmail.com", password=make_password("asd123"),phone="1234567890")
        self.user.save()
        self.suggestion = Suggestions(user=self.user, suggestion="testing suggestion", status="New")
        self.category = Category(category_name="test")
        self.category.save()
        self.suggestion.save()
        self.group = Group(group_name="test", group_desc="test", group_photo_profile_link="test", group_category=self.category)
        self.group.save()
        self.group2 = Group(group_name="test2", group_desc="test2", group_photo_profile_link="test2", group_category=self.category)
        self.group2.save()

        self.init = {
            'email': 'testing@gmail.com',
            'password': 'asd123'
        }
        self.init2 = {
            'email': 'meh@gmail.com',
            'password': 'asd123',
        }

        self.suggestion_init = {
            'id': '1'
        }

        self.suggestion = {
            'suggestion': 'testing suggestion'
        }

        self.init = json.dumps(self.init)
        self.init2 = json.dumps(self.init2)
        self.suggestion_init = json.dumps(self.suggestion_init)
        self.suggestion = json.dumps(self.suggestion)

    
    def test_get_suggestions_is_admin(self):
        response = self.client.post(reverse('login'), self.init, content_type='application/json')
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.get(reverse('get-suggestions'), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
    
    def test_get_suggestions_is_buyerseller(self):
        response = self.client.post(reverse('login'), self.init2, content_type='application/json')
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.get(reverse('get-suggestions'), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        self.assertEquals(response.status_code, 400)
    
    def test_change_suggestions_status(self):
        response = self.client.post(reverse('login'), self.init, content_type='application/json')
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.post(reverse('change-status-suggestions'), self.suggestion_init, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        self.assertEquals(response.status_code, 200)
    
    def test_add_suggestions(self):
        response = self.client.post(reverse('login'), self.init2, content_type='application/json')
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.post(reverse('add-suggestion'), self.suggestion, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        self.assertEquals(response.status_code, 200)
    
    def test_get_all_groups_data(self):
        response = self.client.post(reverse('login'), self.init, content_type='application/json')
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.get(reverse('get-all-groups-data'), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        self.assertEquals(response.status_code, 200)

