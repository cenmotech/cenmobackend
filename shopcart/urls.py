from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('update_to_cart', update_to_cart, name='update_to_cart'),
    path('get_cart', get_cart, name='get_cart'),
    path('get_carts_item/<int:items_id>', get_carts_item, name='get_carts_item'),
    path('get_total_price', get_total_price, name='get_total_price')
]