from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from django.test import SimpleTestCase, TestCase, RequestFactory
from authuser.views import register, login, logout

# Create your tests here.
class TestsUrls(TestCase): 
    def test_url_is_resolved_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)
        
    def test_url_is_resolved_register(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)




