from functools import wraps
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import  status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt, datetime
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import exception_handler


def jwt_authenticated(view_func):
    def wrapper(*args, **kwargs):
        try:
            # Authenticate the user using the access token
            request = args[0]
            user, _ = JWTAuthentication().authenticate(request)
            request.user = user
        except AuthenticationFailed:
            #Raise user not loggeind status response
            return JsonResponse({'message': 'Authentication Failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except TypeError:
            return JsonResponse({'message': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(*args, **kwargs)
    return wrapper


def custom_exception_handler(exc, context):
    if isinstance(exc, InvalidToken) or isinstance(exc.args[0], TokenError):
        # If the error is due to an invalid or expired token, customize the error message
        message = 'Your token has expired or is invalid. Please log in again.'
        code = 'invalid_token'
        return JsonResponse({'detail': message}, status=401, headers={'WWW-Authenticate': f'Bearer realm="{code}"'})
    # For all other exceptions, use Django REST framework's default exception handling
    return exception_handler(exc, context)  
        

