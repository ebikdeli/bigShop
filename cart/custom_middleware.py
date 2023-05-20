"""
Every user connect to the website for the first time, has a cart session created for them.
Important: Before any view called, A Cart and cart sessions must be created for any user either authenticated or Not.
"""
from .cart_functions import get_or_create_cart_unauth_session_key, get_or_create_cart_auth_session_key,\
                            reset_session, get_cart_session
from .models import Cart


class InitialSessionMiddleware:
    """Find the needed sessions for the user and if couldn't find them, create them"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        # ? If session_key has not been created already, create it
        if not request.session.exists(request.session.session_key):
            request.session.create()
        # If cart sessions are not created already, create them
        try:
            get_cart_session(request)
        except KeyError:
            reset_session(request)
        # Get or create Cart for unauthenticated users with the session_key
        if not request.user.is_authenticated:
            cart = get_or_create_cart_unauth_session_key(Cart, request)
        # Get or create Cart object for the athenticated user
        else:
            cart = get_or_create_cart_auth_session_key(Cart, request)
        # If cart is None it means there is a bug in our code
        if cart:
            request.session['cart_id'] = cart.id
        else:
            request.session['cart_id'] = 0
        # print("Cart middle ware last", request.session.items())
        return None
