import datetime
from django.http import HttpResponse
from django.urls import reverse, resolve
from django.test import Client, TestCase, RequestFactory
from django.test import SimpleTestCase, TestCase, RequestFactory
import jwt
from rest_framework import  status
from authuser.views import register, login
from authuser.models import User, Address
from django.contrib.auth.hashers import make_password
import json
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from cenmobackend import settings

class TestViews(TestCase):
    def setUp(self):
        data = {
            "email" : "test@gmail.com",
            "password" : "test123",
            "name" : "test",
            "phone" : "1234567890"
        }

        data2 = {
            "email" : "asd@gmail.com",
            "password" : "asd123",
            'name' : 'meh',
            'phone' : '1234567890'
        }

        data3 = {
             "email" : "asd@gmail.com",
            "password" : "asd12d3"
        }

        data4= {
            "email" : "nah@gmail.com",
            "password" : "nah123"
        }
        data5= {
            "email" : "asd@gmail.com",
            "password" : "asd123"
        }

        admin = {
            "email" : "admin@gmail.com",
            "password" : "admin",
            "name" : "admin",
            "phone" : "1234567890"
        }

        dummy = {
            'name' : 'meh',
            'phone' : '1234567890'
        }

        address = {
                "street":"dadsasdadsasda",
                "city":"dadsasdsaaddsads",
                "province":"adssdadasdsadsaddsa",
                "zip_code":"dsdadsadasdsaddasasdasd",
                "address_name":"nama"
            }
        
        address2 = {
                "street":"dadsasdadsasda",
                "city":"dadsasdsaaddsads",
                "province":"adssdadasdsadsaddsa",
                "zip_code":"dsdadsadasdsaddasasdasd",
                "address_name":"nama2"
            }

        self.user = User(name="meh",email="asd@gmail.com", password=make_password("asd123"),phone="1234567890")
    
        
        self.user.save()

        self.data = json.dumps(data)
        self.data2 = json.dumps(data2)
        self.data3 = json.dumps(data3)
        self.data4 = json.dumps(data4)
        self.data5 = json.dumps(data5)
        self.admin = json.dumps(admin)
        self.dummy = json.dumps(dummy)
        self.address = json.dumps(address)
        self.address2 = json.dumps(address2)

    def test_register_success(self):
        #Make a post request to register endpoint from json data
        response = self.client.post(reverse('register'), self.data, content_type='application/json')
        #Check if response is 201
        self.assertEquals(response.status_code, 201)
        #Check if user is created
        self.assertEquals(User.objects.filter(email="test@gmail.com").get().name, "test")
    
    def test_register_user_exist(self):
        #Make a post request to register endpoint from json data
        response = self.client.post(reverse('register'), self.data2, content_type='application/json')
        #Check if response is 400
        self.assertEquals(response.status_code, 400)
    
    def test_register_method_not_allowed(self):
        #Make a get request to register endpoint
        response = self.client.get(reverse('register'))
        #Check if response is 405
        self.assertEquals(response.status_code, 405)
    
    def test_login_wrong_password(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data3, content_type='application/json')
        #Check if response is 200
        self.assertEquals(response.status_code, 401)

    def test_login_user_does_not_exist(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data4, content_type='application/json')
        #Check if response is 404
        self.assertEquals(response.status_code, 404)
    
    def test_login_method_not_allowed(self):
        #Make a get request to register endpoint
        response = self.client.get(reverse('login'))
        #Check if response is 405
        self.assertEquals(response.status_code, 405)

    def test_login_success(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        #Check if response is 200
        self.assertEquals(response.status_code, 200)
    
    def test_logout_success(self):
        #Make a post request to login endpoint from json data and logout
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        response = self.client.post(reverse('logout'))
        #Check if response is 200
        self.assertEquals(response.status_code, 200)
    
    def test_get_user_session_success(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.get(reverse('get-user-session'), HTTP_AUTHORIZATION='Bearer ' + accessToken)
        #Check if response is 200
        self.assertEquals(response.status_code, 200)
    
    def test_get_user_session_method_not_allowed(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        response = self.client.post(reverse('get-user-session'))
        #Check if response is 405
        self.assertEquals(response.status_code, 405)
    
    def test_get_user_session_not_logged_in(self):
        #Make a get request to get-user-session endpoint
        response = self.client.get(reverse('get-user-session'))
        #Check if response is 401
        self.assertEquals(response.status_code, 401)
    
    def test_register_admin_success(self):
        #Make a post request to register endpoint from json data
        response = self.client.post(reverse('admin-register'), self.admin, content_type='application/json')
        #Check if response is 201
        self.assertEquals(response.status_code, 201)
        #Check if user is created
        self.assertEquals(User.objects.filter(email="admin@gmail.com").get().name, "admin")
    
    def test_register_admin_method_not_allowed(self):
        #Make a get request to register endpoint
        response = self.client.get(reverse('admin-register'))
        #Check if response is 405
        self.assertEquals(response.status_code, 405)
    
    def test_register_admin_user_exist(self):
        #Make a post request to register endpoint from json data
        self.client.post(reverse('admin-register'), self.admin, content_type='application/json')
        response = self.client.post(reverse('admin-register'), self.admin, content_type='application/json')
        #Check if response is 400
        self.assertEquals(response.status_code, 400)
    
    def test_edit_profile_success(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        #Make a put request to edit-profile endpoint from json data
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.post(reverse('edit-profile'), self.dummy, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        #Check if response is 200
        self.assertEquals(response.status_code, 200)
        #Check if user is created
        self.assertEquals(User.objects.filter(email="asd@gmail.com").get().name, "meh")
    
    def test_edit_profile_method_not_allowed(self):
        #Make a get request to edit-profile endpoint
        response = self.client.get(reverse('edit-profile'))

        #Check if response is 405
        self.assertEquals(response.status_code, 405)
    
    def test_get_profile_method_not_allowed(self):
        #Make a post request to get-profile endpoint
        response = self.client.post(reverse('get-user-profile'))
        #Check if response is 405
        self.assertEquals(response.status_code, 405)
    
    def test_add_address_success(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        #Make a post request to add-address endpoint from json data
        # Decode response
        accessToken = json.loads(response.content)['accessToken']
        # Set Authorization header on reverse('add-address')
        
        response = self.client.post(reverse('add-address'), self.address, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        #Check if response is 200
        self.assertEquals(response.status_code, 200)

    def test_get_profile_success(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        #Make a get request to get-profile endpoint
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.post(reverse('add-address'), self.address2, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)

        response = self.client.get(reverse('get-user-profile'), HTTP_AUTHORIZATION='Bearer ' + accessToken)
        #Check if response is 200
        self.assertEquals(response.status_code, 200)
    
    def test_set_main_address(self):
        #Make a post request to login endpoint from json data
        response = self.client.post(reverse('login'), self.data5, content_type='application/json')
        #Make a post request to add-address endpoint from json data
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.post(reverse('add-address'), self.address2, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        #Make a post request to set-main-address endpoint from json data
        response = self.client.post(reverse('set-address', kwargs={"id":1}), self.address2, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        #Check if response is 200
        self.assertEquals(response.status_code, 200)
    






    


    
    

    
        
