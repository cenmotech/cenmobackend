from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.hashers import make_password
from shopcart.models import CartItem
from transaction.views import *
from authuser.models import User, Address
from group.models import Category, Group, Goods



class TestViews(TestCase):
    def setUp(self):
        #Make Goods and Users and save to database
        self.user = User(name="meh",email="testing@gmail.com", password=make_password("asd123"),phone="1234567890")
        self.user.save()
        self.user2 = User(name="meh",email="testings@gmail.com", password=make_password("asd123"),phone="1234567890")
        self.user2.save()
        self.address = Address(user_id=self.user, address_name="testing address", city="testing city", street="testing street", zip_code="123456", province="testing province", is_main=True)
        self.address.save()
        self.category = Category(category_name="testing category")
        self.category.save()
        self.group = Group(group_name="testing group", group_desc="testing group description", group_photo_profile_link="testing group photo profile link", group_category=self.category)
        self.group.save()
        self.good = Goods(goods_name="testing good",goods_description="testing good description", goods_price=10000, goods_image_link="testing good photo profile link", goods_region="region", seller_name="seller", goods_group_origin_id=self.group.group_id, goods_seller_id=self.user)
        self.good.save()
        self.init = {
            'email': 'testing@gmail.com',
            'password': 'asd123'
        }
        self.init2 = {
            'email': 'testings@gmail.com',
            'password': 'asd123'
        }
        self.init = json.dumps(self.init)
        self.init2 = json.dumps(self.init2)
        self.transaction_dummy = Transaction(user_id=self.user, seller_id=self.user,price=10000, total_price=10000, address_user_id=self.address.id,goods_id=self.good.goods_id, transaction_id="TESTING", quantity=1,progress="Pending")
        self.transaction_dummy.save()
        self.cart = Cart(user_id=self.user.email)
        self.cart.save()
        self.cartItem = CartItem(cart_id=self.cart.cart_id, goods_id=self.good.goods_id, quantity=1)
        self.cartItem.save()
        self.cart2 = Cart(user_id=self.user2.email)
        self.cart2.save()


    def test_make_transaction_success(self):
        response = self.client.post(reverse('login'), self.init, content_type='application/json')
        self.body = {'goodId': '1', 'quantity': '1'}
        self.body = json.dumps(self.body)
        accessToken = json.loads(response.content)['accessToken']
        response = self.client.post(reverse('make-transaction'), self.body, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        self.assertEquals(response.status_code, 201)
    
    def test_update_transaction_verifying(self):
        user_response = self.client.post(reverse("login"), self.init, content_type="application/json")
        token = user_response.json().get("accessToken")
        payload = {
            'transactionId': 'TESTING',
            "resi":"1234567890"
        }
        x = Transaction.objects.get(transaction_id="TESTING")
        x.progress = "Verifying"
        x.save()
        self.client.post(reverse('update-transaction'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Transaction.objects.get(transaction_id="TESTING")
        self.assertEqual(target.progress, "Processing")
        self.assertEqual(target.resi, "1234567890")
    
    def test_update_transaction_processing(self):
        user_response = self.client.post(reverse("login"), self.init, content_type="application/json")
        token = user_response.json().get("accessToken")
        payload = {
            'transactionId': 'TESTING',
            "resi":"1234567890"
        }
        self.client.post(reverse('update-transaction'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse('update-transaction'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse('update-transaction'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Transaction.objects.get(transaction_id="TESTING")
        self.assertEqual(target.progress, "Completed")
    
    def test_update_midtrans_settlemen(self):
        user_response = self.client.post(reverse("login"), self.init, content_type="application/json")
        token = user_response.json().get("accessToken")
        target = Transaction.objects.get(transaction_id="TESTING")
        payload = {
            "transaction_time": "2023-04-27 14:31:39",
            "transaction_status": "settlement",
            "transaction_id": "db20d29e-5d94-4f71-9bc4-e96712140f21",
            "status_message": "midtrans payment notification",
            "status_code": "200",
            "signature_key": "e1fc67e28927b99a24166de9b3b4bf5f8f93ecbaf32916ce55802305421a469ea7a28fa3dc59b0d632ac8a005d73857a5762617cd56df75326ecc352f1b8e1eb",
            "order_id": "TESTING",
            "merchant_id": "G044491835",
        }
        self.client.post(reverse('update-midtrans'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Transaction.objects.get(transaction_id="TESTING")
        self.assertEqual(target.progress, "Verifying")
    
    def test_update_midtrans_deny(self):
        user_response = self.client.post(reverse("login"), self.init, content_type="application/json")
        token = user_response.json().get("accessToken")
        target = Transaction.objects.get(transaction_id="TESTING")
        payload = {
            "transaction_time": "2023-04-27 14:31:39",
            "transaction_status": "deny",
            "transaction_id": "db20d29e-5d94-4f71-9bc4-e96712140f21",
            "status_message": "midtrans payment notification",
            "status_code": "200",
            "signature_key": "e1fc67e28927b99a24166de9b3b4bf5f8f93ecbaf32916ce55802305421a469ea7a28fa3dc59b0d632ac8a005d73857a5762617cd56df75326ecc352f1b8e1eb",
            "order_id": "TESTING",
            "merchant_id": "G044491835",
        }
        self.client.post(reverse('update-midtrans'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Transaction.objects.get(transaction_id="TESTING")
        self.assertEqual(target.progress, "Failed")

    def test_update_midtrans_expired(self):
        user_response = self.client.post(reverse("login"), self.init, content_type="application/json")
        token = user_response.json().get("accessToken")
        target = Transaction.objects.get(transaction_id="TESTING")
        payload = {
            "transaction_time": "2023-04-27 14:31:39",
            "transaction_status": "expire",
            "transaction_id": "db20d29e-5d94-4f71-9bc4-e96712140f21",
            "status_message": "midtrans payment notification",
            "status_code": "200",
            "signature_key": "e1fc67e28927b99a24166de9b3b4bf5f8f93ecbaf32916ce55802305421a469ea7a28fa3dc59b0d632ac8a005d73857a5762617cd56df75326ecc352f1b8e1eb",
            "order_id": "TESTING",
            "merchant_id": "G044491835",
        }
        self.client.post(reverse('update-midtrans'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Transaction.objects.get(transaction_id="TESTING")
        self.assertEqual(target.progress, "Expired")
    
    def test_get_seller_transaction(self):
        user_response = self.client.post(reverse("login"), self.init, content_type="application/json")
        token = user_response.json().get("accessToken")
        response = self.client.get(reverse('get-seller-transaction'), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        self.assertEqual(response.status_code, 200)

    def test_make_transaction_no_address(self):
        user_response = self.client.post(reverse("login"), self.init2, content_type="application/json")
        self.body = {'goodId': '1', 'quantity': '1'}
        self.body = json.dumps(self.body)
        accessToken = user_response.json().get("accessToken")
        response = self.client.post(reverse('make-transaction'), self.body, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + accessToken)
        self.assertEquals(response.status_code, 404)


class ComplainTestCase(TestCase):
    def setUp(self):
        user_data = {
            "email" : "dummy@gmail.com",
            "password" : "dummypass",
        }

        self.user_data = json.dumps(user_data)
        user_create = User.objects.create(name="dummy",email="dummy@gmail.com", password=make_password("dummypass"),phone="123456789", is_admin = True)
        self.user_create = user_create
        address = Address.objects.create(user_id=user_create.email, address_name="testing address", city="testing city", street="testing street", zip_code="123456", province="testing province", is_main=True)
        category = Category.objects.create(category_name="testing category")
        group = Group.objects.create(group_name="testing group", group_desc="testing group description", group_photo_profile_link="testing group photo profile link", group_category=category)
        goods = Goods.objects.create(goods_name="testing good", goods_description="testing good description", goods_price=10000, goods_image_link="testing good photo profile link", goods_region="region", seller_name="seller", goods_group_origin_id=group.group_id, goods_seller_id=user_create.email)
        self.transaction_dummy = Transaction(user_id=self.user_create, price=10000, snap_token="1",resi="1",total_price=10000, address_user_id=address.id,goods_id=goods.goods_id, transaction_id="TESTING", quantity=1,progress="Pending")
        self.transaction_dummy.save()  
        self.cart = Cart(user_id=self.user_create)
        self.cart.save()
        self.cartItem = CartItem(cart_id=self.cart.cart_id, goods_id=goods.goods_id, quantity=1)
        self.cartItem.save()

        transaction1 = {
            "transactionId":"TESTING", 
            "user_id":user_create.email, 
            "price":"10000", 
            "total_price":"10000", 
            "address_user_id":address.id,
            "goodId":goods.goods_id, 
            "quantity":1,
            "progress":"Pending",
            "seller":goods.seller_name
        }
        self.transaction1 = json.dumps(transaction1)

        complain1 = {
            "transactionId":"TESTING",
            "user_id":user_create.email,
            "complain_text":"Complain Test",
            "complain_status":"Pending"
        }
        self.complain1 = json.dumps(complain1)

        complainId = {
            "complainId":1
        }
        self.complainId = json.dumps(complainId)

    def test_create_complain(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")
        response = self.client.post(reverse('make-transaction'), self.transaction1, content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEquals(response.status_code, 201)

        complain_response = self.client.post(reverse("create-complain"), self.complain1 , content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        # check response status and message
        self.assertEqual(complain_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(complain_response.json().get("message"), "Complain created successfully")

        # check complain object in database
        complain = Complain.objects.get(transaction_id= self.transaction_dummy.transaction_id, user_id="dummy@gmail.com")
        self.assertEqual(complain.complain_text, "Complain Test")
        self.assertEqual(complain.complain_status, "Pending")
    
    def test_create_complain_fail_no_token(self):
        listing_response = self.client.post(reverse("create-complain"), self.complain1, content_type="application/json")
        self.assertEqual(listing_response.status_code, 401)

    def test_create_complain_fail_token_expired(self):
        listing_response = self.client.post(reverse("create-complain"), self.complain1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InRlc3RAZ21haWwuY29tIiwiZXhwIjoxNjc4ODY3ODEyLCJpYXQiOjE2Nzg4NjQyMTJ9.xIF8t5cdCYmp2NKGvOKs3VqRemCB4FQ59Y9khGYl1DY")
        self.assertEqual(listing_response.status_code, 401)
    
    def test_create_complain_method_not_allowed(self):
        response = self.client.get(reverse("create-complain"))
        self.assertEqual(response.status_code, 405)
    
    def test_get_all_groups_data(self):
        user_response = self.client.post(reverse('login'), self.user_data, content_type='application/json')
        token = user_response.json().get("accessToken")   
        self.client.post(reverse("make-transaction"), self.transaction1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create-complain"), self.complain1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)

        response = self.client.get(reverse('get-complains'), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEquals(response.status_code, 200)

    def test_complain_status_pending(self):

        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")

        self.client.post(reverse("make-transaction"), self.transaction1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create-complain"), self.complain1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        payload = {
            'complain_id': 1
        }
        response = self.client.post(reverse('complain-status'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Complain.objects.get(complain_id=1)
        self.assertEqual(target.complain_status, "Processing")
        self.assertEqual(response.status_code, 201)
    
    
    def test_complain_status_processing(self):
        user_response = self.client.post(reverse("login"), self.user_data, content_type="application/json")
        token = user_response.json().get("accessToken")

        self.client.post(reverse("make-transaction"), self.transaction1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse("create-complain"), self.complain1, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + token)
        payload = {
            'complain_id': 1
        }
        self.client.post(reverse('complain-status'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(reverse('complain-status'), json.dumps(payload), content_type='application/json', HTTP_AUTHORIZATION="Bearer " + token)
        target = Complain.objects.get(complain_id=1)
        self.assertEqual(target.complain_status, "Resolved")