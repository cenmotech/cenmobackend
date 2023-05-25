from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import ensure_csrf_cookie
from .views import *
urlpatterns = [
    path('make-transaction', make_transaction, name='make-transaction'),
    path('update-transaction', update_transaction, name='update-transaction'),
    path('create-complain', create_complain, name='create-complain'),
    path('get-complains', get_complains, name='get-complains'),
    path('complain-status', complain_status, name='complain-status'),
    path('update-midtrans', get_update_from_midtrans, name='update-midtrans'),
    path('get-seller-transaction', get_seller_transaction, name='get-seller-transaction'),
    path('get-buyer-by-goods-id/<int:goods_id>', get_buyer_by_goods_id, name='get_buyer_by_goods_id'),
    path('get_user_transaction', get_user_transaction, name='get_user_transaction'),
    path('get_user_pending_transaction', get_user_pending_transaction, name='get_user_pending_transaction'),
    path('get_user_verifying_transaction', get_user_verifying_transaction, name='get_user_verifying_transaction'),
    path('get_user_processing_transaction', get_user_processing_transaction, name='get_user_processing_transaction'),
    path('get_user_completed_transaction', get_user_completed_transaction, name='get_user_completed_transaction'),
    path('get_user_cancelled_transaction', get_user_cancelled_transaction, name='get_user_cancelled_transaction'),
    path('cancel_transaction', cancel_transaction, name='cancel_transaction'),
    path('finished_transaction', finished_transaction, name='finished_transaction'),
    path('get-bank-list', get_bank_list, name='get_bank_list'),
    path('validate-bank', validate_bank, name='validate_bank'),
    path('add-bank-to-user', add_bank_to_user, name='add_bank_to_user'),
    path('get-user-bank', get_user_bank, name='get_user_bank'),
    path('get-user-withdrawal', get_user_withdrawal, name='get_user_withdrawal'),
    path('update-payout-from-midtrans', update_payout_from_midtrans, name='update_payout_from_midtrans'),
    path('withdraw', withdraw, name='withdraw'),
    # path('testing', testing, name='testing'),
]