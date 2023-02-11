"""
Always send current cart (if exists) to every view
"""
from django.http.request import HttpRequest

from .models import Cart


def get_cart(request: HttpRequest) -> dict:
    """Get current cart for the user or session_key. Returns a context dictionary contains current cart else returns None."""
    # Try get 'cart' if user has authenticated
    cart = None
    if request.user.is_authenticated:
        cart_user_qs = Cart.objects.filter(user=request.user)
        if cart_user_qs.exists():
            cart = cart_user_qs.first()
            return {'cart': cart}
    # If there is a cart with current session_key returns it
    if request.session.session_key:
        cart_session_key_qs = Cart.objects.filter(session_key=request.session.session_key)
        if cart_session_key_qs.exists():
            cart = cart_session_key_qs.get()
    return {'cart': cart}
