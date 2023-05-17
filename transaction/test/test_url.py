from django.test import TestCase
from django.urls import resolve, reverse

from transaction.views import *


class TestsUrls(TestCase):
    def test_url_is_resolved_make_transaction(self):
        url = reverse('make-transaction')
        self.assertEquals(resolve(url).func, make_transaction)

    def test_url_is_resolved_(self):
        url = reverse('update-transaction')
        self.assertEquals(resolve(url).func, update_transaction)

    def test_url_is_resolved_get_snap_token(self):
        url = reverse('update-midtrans')
        self.assertEquals(resolve(url).func, get_update_from_midtrans)
