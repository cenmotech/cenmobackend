from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from django.test import SimpleTestCase, TestCase, RequestFactory
from admincenmo.views import *

# Create your tests here.
class TestsUrls(TestCase): 
    def test_url_is_resolved_get_suggestions(self):
        url = reverse('get-suggestions')
        self.assertEquals(resolve(url).func, get_suggestions)

    def test_url_is_resolved_change_status_suggestions(self):
        url = reverse('change-status-suggestions')
        self.assertEquals(resolve(url).func, change_status_suggestions)

    def test_url_is_resolved_add_suggestion(self):
        url = reverse('add-suggestion')
        self.assertEquals(resolve(url).func, add_suggestion)
    
    def test_url_is_resolved_get_all_groups_data(self):
        url = reverse('get-all-groups-data')
        self.assertEquals(resolve(url).func, get_all_groups_data)




