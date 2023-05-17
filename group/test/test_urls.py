from django.urls import reverse, resolve
from django.test import TestCase
from group.views import *

class TestsUrls(TestCase):
    def test_url_is_resolved_create_group(self):
        url = reverse('create_group')
        self.assertEquals(resolve(url).func, create_group)

    def test_url_is_resolved_create_listing(self):
        url = reverse('create_listing')
        self.assertEquals(resolve(url).func, create_listing)
        
    def test_url_is_resolved_search_group(self):
        url = reverse('search_group', kwargs={'name': 'Group1'})
        self.assertEquals(resolve(url).func, search_group)

    def test_url_is_resolved_see_group(self):
        url = reverse('see_group', kwargs={'group_id': 1})
        self.assertEquals(resolve(url).func, see_group)
        
    def test_url_is_resolved_create_post(self):
        url = reverse('create_post')
        self.assertEquals(resolve(url).func, create_post)

    def test_url_is_resolved_search_post_by_desc(self):
        url = reverse('search_post_by_desc', kwargs={'desc': 'test'})
        self.assertEquals(resolve(url).func, search_post_by_desc)

    def test_url_is_resolved_search_post_on_group(self):
        url = reverse('search_post_on_group', kwargs={'group': 1, 'desc': 'test'})
        self.assertEquals(resolve(url).func, search_post_on_group)

    def test_url_is_resolved_get_post_by_logged_user(self):
        url = reverse('get_post_by_logged_user')
        self.assertEquals(resolve(url).func, get_post_by_logged_user)

    def test_url_is_resolved_get_post_on_group(self):
        url = reverse('get_post_on_group', kwargs={'group': 1})
        self.assertEquals(resolve(url).func, get_post_on_group)
        
    def test_url_is_resolved_search_listing_by_name(self):
        url = reverse('search_listing_by_name', kwargs={'name': 'test'})
        self.assertEquals(resolve(url).func, search_listing_by_name)

    def test_url_is_resolved_search_listing_on_group(self):
        url = reverse('search_listing_on_group', kwargs={'group': 1, 'name': 'test'})
        self.assertEquals(resolve(url).func, search_listing_on_group)

    def test_url_is_resolved_get_listing_by_logged_user(self):
        url = reverse('get_listing_by_logged_user')
        self.assertEquals(resolve(url).func, get_listing_by_logged_user)
    
    def test_url_is_resolved_get_listing_by_seller(self):
        url = reverse('get_listing_by_seller')
        self.assertEquals(resolve(url).func, get_listing_by_seller)

    def test_url_is_resolved_get_listing_by_seller_on_group(self):
        url = reverse('get_listing_by_seller_on_group', kwargs={'group': 1, 'email': 'test@gmail.com'})
        self.assertEquals(resolve(url).func, get_listing_by_seller_on_group)

    def test_url_is_resolved_get_listing_on_group(self):
        url = reverse('get_listing_on_group', kwargs={'group': 1})
        self.assertEquals(resolve(url).func, get_listing_on_group)

    def test_url_is_resolved_join_group(self):
        url = reverse('join_group')
        self.assertEquals(resolve(url).func, join_group)