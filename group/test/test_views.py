from django.test import TestCase, Client
from authuser.models import User
from group.models import Group, Goods, Post, Category, Like, Comment
from django.urls import reverse
from django.contrib.auth.hashers import make_password
import json, jwt
from rest_framework import status

class TestViewsGroup(TestCase):
    def setUp(self):
        user_data = {
            "email" : "dummy@gmail.com",
            "password" : "dummypass",
        }

        user_data_not_admin = {
            "email" : "dummy2@gmail.com",
            "password" : "dummypass2",
        }

        self.user_data = json.dumps(user_data)
        self.user_data_not_admin = json.dumps(user_data_not_admin)
        user = User.objects.create(name="dummy",email="dummy@gmail.com", password=make_password("dummypass"),phone="123456789", is_admin = True)
        user2 = User.objects.create(name="dummy2",email="dummy2@gmail.com", password=make_password("dummypass2"),phone="123456789", is_admin = False)
        self.user = user
        self.user2 = user2
        group1 = {
                        "name" : "Group1",
                        "desc" : "Group 1 Desc",
                        "photo_profile" : "drive.google.com/tempDummyLink",
                        "category" : 1
        }
        group2 = {
                        "name" : "Group2",
                        "desc" : "Desc for Failed Group",
                        "photo_profile" : "drive.google.com/DummyLinkGroupFailed",
                        "category" : 1
        }
        group3 = {
                        "name" : "Group3",
                        "desc" : "Desc for Failed Group",
                        "photo_profile" : "drive.google.com/DummyLinkGroupFailed",
                        "category" : 1
        }
        
        group4 = {
                        "name" : "Group2",
                        "desc" : "Desc for Failed Group",
                        "photo_profile" : "drive.google.com/DummyLinkGroupFailed",
                        "category" : 2
        }

        group5 = {
                        "name" : "Grup2",
                        "desc" : "Desc for Failed Group",
                        "photo_profile" : "drive.google.com/DummyLinkGroupFailed",
                        "category" : 2
        }

        category1 = {
                        "id" : 1,
                        "name" : "Category 1"
        }

        category2 = {
                        "id" : 2,
                        "name" : "Category 2"
        }
        
        self.group1= json.dumps(group1)
        self.group2 = json.dumps(group2)
        self.group3 = json.dumps(group3)
        self.group4 = json.dumps(group4)
        self.group5 = json.dumps(group5)
        self.category1 = json.dumps(category1)
        self.category2 = json.dumps(category2)
    
    def test_create_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        create_response = self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response.status_code, 201)
        self.assertTrue(Group.objects.filter(group_name = "Group1").exists(), True)

    def test_create_group_already_exist(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        
        create_response1 = self.client.post(reverse("create_group"), self.group2, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        create_response2 = self.client.post(reverse("create_group"), self.group2, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response1.status_code, 201)
        self.assertEqual(create_response2.status_code, 400)

    def test_create_group_not_authenticated(self):
        user_response = self.client.post(reverse("login"), self.user_data_not_admin, content_type="application/json")
        token = user_response.json().get("accessToken")
        create_response1 = self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response1.status_code, 401)
    
    def test_create_group_token_expired(self):
        response = self.client.post(reverse('create_group'), self.group3, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(response.status_code, 401)

    def test_create_group_not_allowed(self):
        response = self.client.get(reverse("create_group"))
        self.assertEqual(response.status_code, 405)

    def test_join_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        user = User.objects.get(email = "dummy@gmail.com")
        create_response = self.client.post(reverse("join_group"), {"id":1}, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response.status_code, 200)
        self.assertEqual(Group.objects.filter(group_member = user).exists(), True)

    def test_join_group_already_joined(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        create_response1 = self.client.post(reverse("join_group"), {"id":1}, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        create_response2 = self.client.post(reverse("join_group"), {"id":1}, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response2.status_code, 400)

    def test_join_group_not_authenticated(self):
        response = self.client.post(reverse('join_group'), self.user_data, content_type='application/json')
        self.assertEquals(response.status_code, 401)
    
    def test_join_group_not_allowed(self):
        response = self.client.get(reverse("join_group"))
        self.assertEqual(response.status_code, 405)

    def test_is_joined_return_true(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        self.client.post(reverse("join_group"), {"id":1}, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(reverse("is_joined", kwargs={"group_id": 1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("isMember"), True)

    def test_is_joined_return_false(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        response = self.client.get(reverse("is_joined", kwargs={"group_id": 1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("isMember"), False)
        
    def test_is_join_group_not_authenticated(self):
        response = self.client.post(reverse('is_joined', kwargs={"group_id": 1}), self.user_data, content_type='application/json')
        self.assertEquals(response.status_code, 405)
    
    def test_is_join_group_not_allowed(self):
        response = self.client.get(reverse("is_joined", kwargs={"group_id": 1}))
        self.assertEqual(response.status_code, 401)
    
    def test_create_category_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        create_response = self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response.status_code, 201)
        self.assertTrue(Category.objects.filter(category_name = "Category 1").exists(), True)

    def test_search_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        search_response = self.client.get(reverse("search_group", kwargs={"name":"Group1"}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.json().get("response")[0].get("group_name"), "Group1")


    def test_search_group_fail_no_token(self):
        search_response = self.client.get(reverse("search_group", kwargs={"name":"Group1"}))
        self.assertEqual(search_response.status_code, 401)

    def test_search_group_fail_token_expired(self):
        search_response = self.client.get(reverse("search_group", kwargs={"name":"Group1"}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_search_group_method_not_allowed(self):
        response = self.client.post(reverse("search_group", kwargs={"name":"Group1"}))
        self.assertEqual(response.status_code, 405)

    def test_see_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        search_response = self.client.get(reverse("see_group", kwargs={"group_id":1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.json().get("response").get("group_name"), "Group1")
    
    def test_see_group_fail_no_token(self):
        search_response = self.client.get(reverse("see_group", kwargs={"group_id":1}))
        self.assertEqual(search_response.status_code, 401)

    def test_see_group_fail_token_expired(self):
        search_response = self.client.get(reverse("see_group", kwargs={"group_id":1}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_see_group_method_not_allowed(self):
        response = self.client.post(reverse("see_group", kwargs={"group_id":1}))
        self.assertEqual(response.status_code, 405)

    def test_get_category_contains_on_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")

        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_category"), self.category2, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group4, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group5, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        
        get_response = self.client.get(reverse("get_all_categories_contains", kwargs={"keyword":"up2"}),HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json(), {'category_groups': {
            'Category 2': [{'group_name': 'Group2', 'group_id': 2}, {'group_name': 'Grup2', 'group_id': 3}]
        }})

    def test_get_category_contains_on_group_fail_no_token(self):
        get_response = self.client.get(reverse("get_all_categories_contains", kwargs={"keyword":"up2"}))
        self.assertEqual(get_response.status_code, 401)

    def test_get_category_contains_on_group_fail_token_expired(self):
        get_response = self.client.get(reverse("get_all_categories_contains", kwargs={"keyword":"up2"}), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_category_contains_on_group_method_not_allowed(self):
        response = self.client.post(reverse("get_all_categories_contains", kwargs={"keyword":"up2"}))
        self.assertEqual(response.status_code, 405)

    def test_create_category_already_exist(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        create_response1 = self.client.post(reverse("create_category"), self.category2, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        create_response2 = self.client.post(reverse("create_category"), self.category2, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response1.status_code, 201)
        self.assertEqual(create_response2.status_code, 400)

    def test_create_category_not_authenticated(self):
        user_response = self.client.post(reverse("login"), self.user_data_not_admin, content_type="application/json")
        token = user_response.json().get("accessToken")
        create_response1 = self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(create_response1.status_code, 401)
    
    def test_create_category_token_expired(self):
        response = self.client.post(reverse('create_category'), self.category1, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(response.status_code, 401)

    def test_create_category_not_allowed(self):
        response = self.client.get(reverse("create_category"))
        self.assertEqual(response.status_code, 405)

    def test_get_category_on_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")

        self.client.post(reverse("create_category"), self.category1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_category"), self.category2, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        self.client.post(reverse("create_group"), self.group1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group4, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_group"), self.group3, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        
        get_response = self.client.get(reverse("get_all_categories"), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json(), {'category_groups': [{'category_name': 'Category 1', 'category_id': 1}, {'category_name': 'Category 2', 'category_id': 2}]})

    def test_get_category_on_group_fail_no_token(self):
        get_response = self.client.get(reverse("get_all_categories"))
        self.assertEqual(get_response.status_code, 401)

    def test_get_category_on_group_fail_token_expired(self):
        get_response = self.client.get(reverse("get_all_categories"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_category_on_group_method_not_allowed(self):
        response = self.client.post(reverse("get_all_categories"))
        self.assertEqual(response.status_code, 405)

class TestListing(TestCase):
    def setUp(self):
        user_data = {
            "email" : "user@gmail.com",
            "password" : "user"
        }
        self.user_data = json.dumps(user_data)
        user = User.objects.create(name="user",email="user@gmail.com", password=make_password("user"),phone="123456789")
        self.user = user
        category = Category.objects.create(category_name = "Category 1")
        Group.objects.create(group_name = "Kamera", group_desc = "Forum untuk jual beli kamera", group_photo_profile_link = "drive.google.com/tempDummyLink", group_category = category)
        camera_data1 = {
                        "name" : "Kamera Nikon",
                        "price" : 5000000,
                        "desc" : "Second like new",
                        "image" : "drive.google.com/axwadawdaw",
                        "region" : "Jakarta",
                        "group" : 1,
                        "stock" : 1
        }
        camera_data2 = {
                        "name" : "Kamera Canon",
                        "price" : 5000000,
                        "desc" : "Second like new",
                        "image" : "drive.google.com/axwadawdaw",
                        "region" : "Jakarta",
                        "group" : 1,
                        "stock" : 1
        }
        camera_data3 = {
                        "id"    : 1,
                        "name" : "Kamera Sony",
                        "price" : 5000000,
                        "desc" : "Second like new",
                        "image" : "drive.google.com/axwadawdaw",
                        "region" : "Jakarta",
                        "group" : 1,
                        "stock" : 1
        }
        self.camera_data1 = json.dumps(camera_data1)
        self.camera_data2 = json.dumps(camera_data2)
        self.camera_data3 = json.dumps(camera_data3)
    
    def test_create_listing_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        listing_response = self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(listing_response.status_code, 201)
        self.assertEqual(Goods.objects.get(goods_name = "Kamera Nikon").goods_seller, self.user)

    def test_create_listing_fail_no_token(self):
        listing_response = self.client.post(reverse("create_listing"), self.camera_data2, content_type="application/json")
        self.assertEqual(listing_response.status_code, 401)

    def test_create_listing_fail_token_expired(self):
        listing_response = self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(listing_response.status_code, 401)
    
    def test_create_listing_method_not_allowed(self):
        response = self.client.get(reverse("create_listing"))
        self.assertEqual(response.status_code, 405)

    def test_search_listing_by_name_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        search_response = self.client.get(reverse("search_listing_by_name", kwargs={"name":"Kamera"}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_search_listing_by_name_fail_no_token(self):
        search_response = self.client.get(reverse("search_listing_by_name", kwargs={"name":"Kamera"}))
        self.assertEqual(search_response.status_code, 401)

    def test_search_listing_by_name_fail_token_expired(self):
        search_response = self.client.get(reverse("search_listing_by_name", kwargs={"name":"Kamera"}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_search_listing_by_name_method_not_allowed(self):
        response = self.client.post(reverse("search_listing_by_name", kwargs={"name":"Kamera"}))
        self.assertEqual(response.status_code, 405)
    
    def test_search_listing_by_seller_and_name_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        search_response = self.client.get(reverse("search_listing_by_seller_and_name", kwargs={"name":"Kamera"}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_search_listing_by_seller_and_name_fail_no_token(self):
        search_response = self.client.get(reverse("search_listing_by_seller_and_name", kwargs={"name":"Kamera"}))
        self.assertEqual(search_response.status_code, 401)

    def test_search_listing_by_seller_and_name_fail_token_expired(self):
        search_response = self.client.get(reverse("search_listing_by_seller_and_name", kwargs={"name":"Kamera"}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_search_listing_by_seller_and_name_method_not_allowed(self):
        response = self.client.post(reverse("search_listing_by_seller_and_name", kwargs={"name":"Kamera"}))
        self.assertEqual(response.status_code, 405)

    def test_search_listing_on_group_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        search_response = self.client.get(reverse("search_listing_on_group", kwargs={"group":1, "name":"Kamera"}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_search_listing_on_group_fail_no_token(self):
        search_response = self.client.get(reverse("search_listing_on_group", kwargs={"group":1, "name":"Kamera"}))
        self.assertEqual(search_response.status_code, 401)

    def test_search_listing_on_group_fail_token_expired(self):
        search_response = self.client.get(reverse("search_listing_on_group", kwargs={"group":1, "name":"Kamera"}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_search_listing_on_group_method_not_allowed(self):
        response = self.client.post(reverse("search_listing_on_group", kwargs={"group":1, "name":"Kamera"}))
        self.assertEqual(response.status_code, 405)

    def test_get_listing_by_logged_user_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(reverse("get_listing_by_logged_user"), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_get_listing_by_logged_user_fail_no_token(self):
        get_response = self.client.get(reverse("get_listing_by_logged_user"))
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_by_logged_user_fail_token_expired(self):
        get_response = self.client.get(reverse("get_listing_by_logged_user"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_by_logged_user_method_not_allowed(self):
        response = self.client.post(reverse("get_listing_by_logged_user"))
        self.assertEqual(response.status_code, 405)
    
    def test_edit_listing_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(reverse('edit_listing'), self.camera_data3, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Goods.objects.filter(goods_id=1).get().goods_name, "Kamera Sony")
    
    def test_edit_listing_method_not_allowed(self):
        response = self.client.get(reverse('edit_listing'))
        self.assertEquals(response.status_code, 405)

    def test_get_listing_by_seller(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(reverse("get_listing_by_seller"), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_get_listing_by_seller_fail_no_token(self):
        get_response = self.client.get(reverse("get_listing_by_seller"))
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_by_seller_fail_token_expired(self):
        get_response = self.client.get(reverse("get_listing_by_seller"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_by_seller_method_not_allowed(self):
        response = self.client.post(reverse("get_listing_by_seller"))
        self.assertEqual(response.status_code, 405)

    def test_get_listing_by_seller_on_group(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(reverse("get_listing_by_seller_on_group", kwargs={"email":"user@gmail.com", "group":1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_get_listing_by_seller_on_group_fail_no_token(self):
        get_response = self.client.get(reverse("get_listing_by_seller_on_group", kwargs={"email":"user@gmail.com", "group":1}))
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_by_seller_on_group_fail_token_expired(self):
        get_response = self.client.get(reverse("get_listing_by_seller_on_group", kwargs={"email":"user@gmail.com", "group":1}), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_by_seller_on_group_method_not_allowed(self):
        response = self.client.post(reverse("get_listing_by_seller_on_group", kwargs={"email":"user@gmail.com", "group":1}))
        self.assertEqual(response.status_code, 405)

    def test_get_listing_on_group(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(reverse("get_listing_on_group", kwargs={"group":1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")

    def test_get_listing_on_group_fail_no_token(self):
        get_response = self.client.get(reverse("get_listing_on_group", kwargs={"group":1}))
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_on_group_fail_token_expired(self):
        get_response = self.client.get(reverse("get_listing_on_group", kwargs={"group":1}), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_listing_on_group_method_not_allowed(self):
        response = self.client.post(reverse("get_listing_on_group", kwargs={"group":1}))
        self.assertEqual(response.status_code, 405)

    def test_get_store(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")

        self.client.post(reverse("join_group"), {"id":1}, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create_listing"), self.camera_data1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(reverse("get_store"), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("response")[0].get("goods_name"), "Kamera Nikon")
    
    def test_get_store_fail_no_token(self):
        get_response = self.client.get(reverse("get_store"))
        self.assertEqual(get_response.status_code, 401)

    def test_get_store_fail_token_expired(self):
        get_response = self.client.get(reverse("get_store"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_store_method_not_allowed(self):
        response = self.client.post(reverse("get_store"))
        self.assertEqual(response.status_code, 405)  

class TestPost(TestCase):
    def setUp(self):
        user_data = {
            "email" : "user@gmail.com",
            "password" : "user"
        }
        another_user_data = {
            "email" : "anotheruser@gmail.com",
            "password" : "anotheruser"
        }
        self.user_data = json.dumps(user_data)
        self.another_user_data = json.dumps(another_user_data)
        user = User.objects.create(name="user",email="user@gmail.com", password=make_password("user"),phone="123456789")
        another_user = User.objects.create(name="anotheruser",email="anotheruser@gmail.com", password=make_password("anotheruser"),phone="987654321")
        self.user = user
        self.another_user = another_user
        category = Category.objects.create(category_name = "Category 1")
        game_group = Group.objects.create(group_name = "Game", group_desc = "Forum untuk jual beli dan diskusi game", group_photo_profile_link = "drive.google.com/tempDummyLink", group_category = category)
        self.group = game_group
        post_data = {
            "desc": "Test post description",
            "image": "https://example.com/image.jpg",
            "group": self.group.group_id,
            "tags": []
        }
        self.post_data = json.dumps(post_data)

    def test_create_post_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        post_response = self.client.post(reverse('create_post'),self.post_data,content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(Post.objects.get(post_desc='Test post description').post_desc, 'Test post description')

    def test_create_post_not_authenticated(self):
        create_response1 = self.client.post(reverse("create_post"), self.post_data, content_type="application/json")
        self.assertEqual(create_response1.status_code, 401)
    
    def test_create_post_method_not_allowed(self):
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 405)

    # def test_search_post_by_desc_success(self):
    #     user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
    #     token = user_response.json().get("accessToken")
    #     self.client.post(reverse("create_post"), self.post_data, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

    #     search_response = self.client.get(reverse("search_post_by_desc", kwargs={"desc":"Test"}), HTTP_AUTHORIZATION="Bearer " + token)
    #     self.assertEqual(search_response.status_code, 200)
    #     self.assertEqual(search_response.json().get("response")[0].get("post_desc"), "Test post description")

    def test_search_post_by_desc_fail_no_token(self):
        search_response = self.client.get(reverse("search_post_by_desc", kwargs={"desc":"Test"}))
        self.assertEqual(search_response.status_code, 401)

    def test_search_post_by_desc_fail_token_expired(self):
        search_response = self.client.get(reverse("search_post_by_desc", kwargs={"desc":"Test"}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_search_post_by_desc_method_not_allowed(self):
        response = self.client.post(reverse("search_post_by_desc", kwargs={"desc":"Test"}))
        self.assertEqual(response.status_code, 405)

    # def test_search_post_on_group_success(self):
    #     user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
    #     token = user_response.json().get("accessToken")
    #     self.client.post(reverse("create_post"), self.post_data, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

    #     search_response = self.client.get(reverse("search_post_on_group", kwargs={"group":1,"desc":"Test"}), HTTP_AUTHORIZATION="Bearer " + token)
    #     self.assertEqual(search_response.status_code, 200)
    #     self.assertEqual(search_response.json().get("response")[0].get("post_desc"), "Test post description")

    def test_search_post_on_group_fail_no_token(self):
        search_response = self.client.get(reverse("search_post_on_group", kwargs={"group":1,"desc":"Test"}))
        self.assertEqual(search_response.status_code, 401)

    def test_search_post_on_group_fail_token_expired(self):
        search_response = self.client.get(reverse("search_post_on_group", kwargs={"group":1,"desc":"Test"}), HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(search_response.status_code, 401)

    def test_search_post_on_group_method_not_allowed(self):
        response = self.client.post(reverse("search_post_on_group", kwargs={"group":1,"desc":"Test"}))
        self.assertEqual(response.status_code, 405)

    # def test_get_post_by_logged_user_success(self):
    #     user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
    #     token = user_response.json().get("accessToken")
    #     self.client.post(reverse("create_post"), self.post_data, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

    #     get_response = self.client.get(reverse("get_post_by_logged_user"), HTTP_AUTHORIZATION="Bearer " + token)
    #     self.assertEqual(get_response.status_code, 200)
    #     self.assertEqual(get_response.json().get("response")[0].get("post_desc"), "Test post description")

    def test_get_post_by_logged_user_fail_no_token(self):
        get_response = self.client.get(reverse("get_post_by_logged_user"))
        self.assertEqual(get_response.status_code, 401)

    def test_get_post_by_logged_user_fail_token_expired(self):
        get_response = self.client.get(reverse("get_post_by_logged_user"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_post_by_logged_user_method_not_allowed(self):
        response = self.client.post(reverse("get_post_by_logged_user"))
        self.assertEqual(response.status_code, 405)

    # def test_get_post_on_group(self):
    #     user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
    #     token = user_response.json().get("accessToken")
    #     self.client.post(reverse("create_post"), self.post_data, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

    #     get_response = self.client.get(reverse("get_post_on_group", kwargs={"group":1}), HTTP_AUTHORIZATION="Bearer " + token)
    #     self.assertEqual(get_response.status_code, 200)
    #     self.assertEqual(get_response.json().get("response")[0].get("post_desc"), "Test post description")

    def test_get_post_on_group_fail_no_token(self):
        get_response = self.client.get(reverse("get_post_on_group", kwargs={"group":1}))
        self.assertEqual(get_response.status_code, 401)

    def test_get_post_on_group_fail_token_expired(self):
        get_response = self.client.get(reverse("get_post_on_group", kwargs={"group":1}), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_post_on_group_method_not_allowed(self):
        response = self.client.post(reverse("get_post_on_group", kwargs={"group":1}))
        self.assertEqual(response.status_code, 405)

    def test_delete_post_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_post"), self.post_data, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(reverse("delete_post", kwargs={"group":1,"postingan_id":1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
    
    def test_delete_post_fail_token_expired(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        self.client.post(reverse("create_post"), self.post_data, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        another_user = self.client.post(reverse("login"), self.another_user_data, content_type="application/json")
        invalid_token = another_user.json().get("accessToken")

        get_response = self.client.get(reverse("delete_post", kwargs={"group":1,"postingan_id":1}), HTTP_AUTHORIZATION="Bearer " + invalid_token)
        self.assertEqual(get_response.status_code, 401)

    # def test_get_feed(self):
    #     user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
    #     token = user_response.json().get("accessToken")
    #     self.client.post(reverse("join_group"), {"id":1}, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

    #     get_response = self.client.get(reverse("get_feed"), HTTP_AUTHORIZATION="Bearer " + token)
    #     self.assertEqual(get_response.status_code, 200)

    
    def test_get_feed_fail_no_token(self):
        get_response = self.client.get(reverse("get_feed"))
        self.assertEqual(get_response.status_code, 401)

    def test_get_feed_fail_token_expired(self):
        get_response = self.client.get(reverse("get_feed"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_feed_method_not_allowed(self):
        response = self.client.post(reverse("get_feed"))
        self.assertEqual(response.status_code, 405)

class TestLike(TestCase):
    def setUp(self):
        user_data1 = {
            "email" : "user1@gmail.com",
            "password" : "user1"
        }
        user_data2 = {
            "email" : "user2@gmail.com",
            "password" : "user2"
        }
        self.user_data = json.dumps(user_data1)
        self.user_data2 = json.dumps(user_data2)
        user1 = User.objects.create(name="user1",email="user1@gmail.com", password=make_password("user1"),phone="123456789")
        user2 = User.objects.create(name="user2",email="user2@gmail.com", password=make_password("user2"),phone="123456789")
        self.user1 = user1
        self.user2 = user2

        category = Category.objects.create(category_name = "Category 1")
        group = Group.objects.create(group_name = "Kamera", group_desc = "Forum untuk jual beli kamera", group_photo_profile_link = "drive.google.com/tempDummyLink", group_category = category)
        post1 = Post.objects.create(post_desc = "Test post description", post_image_link = "https://example.com/image.jpg", post_group_origin= group, post_user=user1)
        post2 = Post.objects.create(post_desc = "Second test post description", post_image_link = "https://example.com/image.jpg", post_group_origin= group, post_user=user2)
        self.post1 = post1
        self.post2 = post2
        
        like_data1 = {
                        "like_id" : 1,
                        "like_post" : post1.post_id,
                        "like_user" : user1.email
        }
        like_data2 = {
                        "like_id" : 2,
                        "like_post" : post2.post_id,
                        "like_user" : user1.email
        }
        like_data3 = {
                        "like_id" : 1,
                        "like_post" : post1.post_id,
                        "like_user" : user2.email
        }

        self.like_data1 = json.dumps(like_data1)
        self.like_data2 = json.dumps(like_data2)
        self.like_data3 = json.dumps(like_data3)

    def test_like_post(self):
        # check user authentication
        user_response = self.client.post(reverse('login'), self.user_data, content_type='application/json')
        token = user_response.json().get("accessToken")
        
        # like post
        response = self.client.post(reverse("like", kwargs={"post_id":1}), content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Post Liked')
        
        # check post likes
        post = Post.objects.get(post_id=self.post1.post_id)
        self.assertEqual(post.post_likes, 1)
        
        # unlike post
        response = self.client.post(reverse("like", kwargs={"post_id":1}), content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Post Unliked')
        
        # check post likes
        post = Post.objects.get(post_id=self.post1.post_id)
        self.assertEqual(post.post_likes, 0)
        
        # like post again
        response = self.client.post(reverse("like", kwargs={"post_id":1}), content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Post Liked')
        
        # check post likes
        post = Post.objects.get(post_id=self.post1.post_id)
        self.assertEqual(post.post_likes, 1)
        
        # unlike post again
        response = self.client.post(reverse("like", kwargs={"post_id":1}), content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Post Unliked')
        
        # Check that the post_likes count was updated correctly
        post = Post.objects.get(post_id=1)
        self.assertEqual(post.post_likes, 0)

    def test_like_fail_no_token(self):
        get_response = self.client.get(reverse("like", kwargs={"post_id":1}))
        self.assertEqual(get_response.status_code, 405)

    def test_like_fail_token_expired(self):
        get_response = self.client.get(reverse("like", kwargs={"post_id":1}), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_like_not_allowed(self):
        response = self.client.post(reverse("like", kwargs={"post_id":1}))
        self.assertEqual(response.status_code, 401)
    
    def test_like_by_user(self):
        # check user authentication
        user_response = self.client.post(reverse('login'), self.user_data, content_type='application/json')
        token = user_response.json().get("accessToken")

        # like post
        response = self.client.post(reverse("like", kwargs={"post_id":1}), content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Post Liked')

        response = self.client.get(reverse("liked_by_user"), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_like_by_user_fail_no_token(self):
        get_response = self.client.get(reverse("liked_by_user"))
        self.assertEqual(get_response.status_code, 401)

    def test_like_by_user_fail_token_expired(self):
        get_response = self.client.get(reverse("liked_by_user"), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_like_by_user_not_allowed(self):
        response = self.client.post(reverse("liked_by_user"))
        self.assertEqual(response.status_code, 405)

class TestComment(TestCase):
    def setUp(self):
        user_data1 = {
            "email" : "user1@gmail.com",
            "password" : "user1"
        }
        user_data2 = {
            "email" : "user2@gmail.com",
            "password" : "user2"
        }
        self.user_data = json.dumps(user_data1)
        self.user_data2 = json.dumps(user_data2)
        user1 = User.objects.create(name="user1",email="user1@gmail.com", password=make_password("user1"),phone="123456789")
        user2 = User.objects.create(name="user2",email="user2@gmail.com", password=make_password("user2"),phone="123456789")
        self.user1 = user1
        self.user2 = user2

        category = Category.objects.create(category_name = "Category 1")
        group = Group.objects.create(group_name = "Kamera", group_desc = "Forum untuk jual beli kamera", group_photo_profile_link = "drive.google.com/tempDummyLink", group_category = category)
        post1 = Post.objects.create(post_desc = "Test post description", post_image_link = "https://example.com/image.jpg", 
                                    post_group_origin= group, post_user=user1)
        post2 = Post.objects.create(post_desc = "Second test post description", post_image_link = "https://example.com/image.jpg", 
                                    post_group_origin= group, post_user=user2)
        self.post1 = post1
        self.post2 = post2
        
        comment_data1 = {
                        "comment_id" : 1,
                        "comment_post" : post1.post_id,
                        "comment_user" : user1.email,
                        "comment_text" : "Comment 1",
                        "user_username" : user1.username
        }
        comment_data2 = {
                        "comment_id" : 2,
                        "comment_post" : post2.post_id,
                        "comment_user" : user2.email,
                        "comment_text" : "Comment 2",
                        "user_username" : user2.username
        }
        comment_data3 = {
                        "comment_id" : 1,
                        "comment_post" : post1.post_id,
                        "comment_user" : user1.email,
                        "comment_text" : "Comment 3",
                        "user_username" : user1.username
        }

        self.comment_data1 = json.dumps(comment_data1)
        self.comment_data2 = json.dumps(comment_data2)
        self.comment_data3 = json.dumps(comment_data3)

    def test_comment_success(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")

        comment_response = self.client.post(reverse('comment', kwargs={"post_id":1}),self.comment_data1,content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(comment_response.status_code, 200)
        self.assertEqual(Comment.objects.get(comment_text='Comment 1').comment_text, 'Comment 1')

    def test_comment_not_authenticated(self):
        create_response1 = self.client.post(reverse("comment", kwargs={"post_id":1}), self.comment_data1, content_type="application/json")
        self.assertEqual(create_response1.status_code, 401)
    
    def test_comment_method_not_allowed(self):
        response = self.client.get(reverse("comment", kwargs={"post_id":1}))
        self.assertEqual(response.status_code, 405)
    
    def test_get_comment(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        comment_response = self.client.post(reverse('comment', kwargs={"post_id":1}),self.comment_data1,content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(comment_response.status_code, 200)
        self.assertEqual(Comment.objects.get(comment_text='Comment 1').comment_text, 'Comment 1')
        get_response = self.client.get(reverse("get_comment", kwargs={"post_id":1}), HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("response")[0].get("comment_text"), "Comment 1")

    def test_get_comment_fail_no_token(self):
        get_response = self.client.get(reverse("get_comment", kwargs={"post_id":1}))
        self.assertEqual(get_response.status_code, 401)

    def test_get_comment_fail_token_expired(self):
        get_response = self.client.get(reverse("get_comment", kwargs={"post_id":1}), HTTP_AUTHORIZATION= "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(get_response.status_code, 401)

    def test_get_comment_method_not_allowed(self):
        response = self.client.post(reverse("get_comment", kwargs={"post_id":1}))
        self.assertEqual(response.status_code, 405)