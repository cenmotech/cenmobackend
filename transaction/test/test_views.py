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

    def test_get_snap_token_success(self):
        token = create_snap_token("TEST123", 10000)
        self.assertIsNotNone(token)
    
    
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
            "transaction_status": "expired",
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
