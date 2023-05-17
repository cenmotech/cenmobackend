from django.urls import reverse, resolve
from django.test import TestCase
from shopcart.views import *

class TestsUrls(TestCase):
    def test_url_is_resolved_update_to_cart(self):
        url = reverse('update_to_cart')
        self.assertEquals(resolve(url).func, update_to_cart)

    def test_url_is_resolved_get_cart(self):
        url = reverse('get_cart')
        self.assertEquals(resolve(url).func, get_cart)