"""
This module defines 'login' function. This function used to login users in the 'normal django views' with 'DRF authtoken'.
With this function we can integrate normal django views authentication with DRF token based authentication.
"""
from django.contrib.auth import login
from rest_framework.authtoken.models import Token

def token_login(request):
    """
    Login users with token header:: log_in(request)->tuple(bool, str)
    """
    if not request.user.is_authenticated:
        try:
            token_header = request.headers.get('Authorization', None)
            if token_header:
                token_key = token_header.split()[1]
                token_obj = Token.objects.filter(key=token_key)
                if token_obj.exists():
                    token = token_obj.first()
                    login(request, token.user)
                else:
                    return False, 'No token found with the key'
            else:
                return False, 'No authentication made'
        except AttributeError:
            return False, 'No user authenticated'
    else:
        return True, 'user has already authencticated'
    return True, request.user.username
