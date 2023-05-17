from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('create_group', create_group, name='create_group'),
    path('create_post', create_post, name='create_post'),
    path('create_listing', create_listing, name='create_listing'),
    path('create_category', create_category, name='create_category'),
    path('get_all_categories', get_all_categories, name='get_all_categories'),
    path('search_post_by_desc/<str:desc>/', search_post_by_desc, name='search_post_by_desc'),
    path('search_post_on_group/<int:group>/<str:desc>/', search_post_on_group, name='search_post_on_group'),
    path('get_post_by_logged_user', get_post_by_logged_user, name='get_post_by_logged_user'),
    path('get_post_on_group/<int:group>', get_post_on_group, name='get_post_on_group'),
    path('search_listing_by_name/<str:name>/', search_listing_by_name, name='search_listing_by_name'),
    path('search_listing_by_seller_and_name/<str:name>/', search_listing_by_seller_and_name, name='search_listing_by_seller_and_name'),
    path('search_listing_on_group/<int:group>/<str:name>/', search_listing_on_group, name='search_listing_on_group'),
    path('get_listing_by_logged_user', get_listing_by_logged_user, name='get_listing_by_logged_user'),
    path('get_listing_by_seller', get_listing_by_seller, name='get_listing_by_seller'),
    path('get_listing_by_seller_on_group/<int:group>/<str:email>', get_listing_by_seller_on_group, name='get_listing_by_seller_on_group'),
    path('get_listing_on_group/<int:group>', get_listing_on_group, name='get_listing_on_group'),
    path('edit_listing', edit_listing, name='edit_listing'),
    path('join_group', join_group, name='join_group'),
    path('is_joined/<int:group_id>', is_joined, name='is_joined'),
    path('search_group/<str:name>', search_group, name='search_group'),
    path('see_group/<int:group_id>', see_group, name='see_group'),
    path('get_all_categories_contains/<str:keyword>', get_all_categories_contains, name='get_all_categories_contains'),
    path('delete_post/<int:group>/<int:postingan_id>', delete_post, name='delete_post'),
    path('get_feed', get_feed, name='get_feed'),
    path('get_store', get_store, name='get_store'),
    path('like/<int:post_id>', like, name='like'),
    path('comment/<int:post_id>', comment, name='comment'),
    path('get_comment/<int:post_id>', get_comment, name='get_comment'),
    path('liked_by_user', liked_by_user, name='liked_by_user'),
]
