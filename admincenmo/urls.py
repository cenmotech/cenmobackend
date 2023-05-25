from django.urls import path
from django.urls.conf import include
from django.views.decorators.csrf import ensure_csrf_cookie
from .views import *
urlpatterns = [
    path('get-suggestions', get_suggestions, name='get-suggestions'),
    path('change-status-suggestions', change_status_suggestions, name='change-status-suggestions'),
    path('add-suggestion', add_suggestion, name='add-suggestion'),
    path('get-all-groups-data', get_all_groups_data, name='get-all-groups-data'),
    path('get-all-categories-for-admin', get_all_categories_for_admin, name='get_all_categories_for_admin'),
]