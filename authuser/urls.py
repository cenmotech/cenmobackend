from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import ensure_csrf_cookie
from .views import register, login, logout, get_user_session, register_admin, edit_profile, get_user_profile, add_address

urlpatterns = [
    path('register', register, name='register'),
    path('admin-register', register_admin, name='admin-register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('get-user-session', get_user_session, name='get-user-session'),
    path('edit-profile', edit_profile, name='edit-profile'),
    path('get-user-profile', get_user_profile, name='get-user-profile'),
    path('add-address', add_address, name='add-address'),
]
