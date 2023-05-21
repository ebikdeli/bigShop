"""
Functions used for clean code practice and reusability. 'cart_id' session needed to hold value of the current cart
"""
from django.http.request import HttpRequest


def get_cart_session(request: HttpRequest) -> None:
    """Get all 'cart' sessions"""
    request.session['cart']
    request.session['total_quantity']
    request.session['price']
    request.session['price_end']


def reset_session(request: HttpRequest) -> None:
    """Reset all sessions to default value"""
    request.session['cart'] = dict()
    request.session['total_quantity'] = 0
    request.session['price'] = 0
    request.session['price_end'] = 0


def set_session_cart(request: HttpRequest, cart: object) -> None:
    """Set cart session values to Cart fields values. 'cart' is an instance of Cart"""
    request.session['total_quantity'] = cart.total_quantity
    request.session['price'] = int(cart.price)
    request.session['price_end'] = int(cart.price_end)


def get_cart_with_id(_model: object, cart_id: int) -> object or None:
    """Get 'Cart' object as '_model' with 'Cart.id' as 'cart_id' field. If 'id' is correct, returns Cart object otherwise
    returns None"""
    cart_qs = _model.objects.filter(id=cart_id)
    # cart_qs = Cart.objects.filter(id=cart_id)
    if cart_qs.exists():
        return cart_qs.get()
    return None


def get_or_create_cart_unauth_session_key(_model: object, request: HttpRequest) -> object:
    """Get 'Cart' as '_model'. Get or create Cart object for 'unauthenticated' user with 'session_key'.
    If successful returns Cart object else returns None"""
    cart = None
    cart_qs = _model.objects.filter(session_key=request.session.session_key)
    # cart_qs = Cart.objects.filter(session_key=request.session.session_key)
    if not cart_qs.exists():
        cart = _model.objects.create(session_key=request.session.session_key)
        print('cart created for unuser')
        # cart = Cart.objects.create(session_key=request.session.session_key)
    else:
        cart = cart_qs.get()
    return cart


def get_or_create_cart_auth_session_key(_model: object, request: HttpRequest) -> object:
    """Get 'Cart' as '_model'. Get or create Cart object for 'authenticated' user with 'session_key'.
    If successful returns Cart object else returns None"""
    cart = None
    cart_qs = _model.objects.filter(user=request.user)
    # cart_qs = Cart.objects.filter(user=request.user)
    # If current user does not have any Cart, get a Cart with current 'session_key' and set current user as its user
    if not cart_qs.exists():
        cart_session = _model.objects.filter(session_key=request.session.session_key)
        # cart_session = Cart.objects.filter(session_key=request.session.session_key)
        # If there is no Cart with current session_key either, create a new Cart with current user and current session_key
        if not cart_session.exists():
            # ? If session_key has not been created already, create it
            print('SESSION_KEY: ', request.session.session_key)
            if not request.session.exists(request.session.session_key):
                session_key = request.session.create()
            cart = _model.objects.create(user=request.user, session_key=request.session.session_key)
            print('cart created for the user')
            # !Changed after using ajax
            reset_session(request)
            
            # Cart.objects.create(user=request.user, session_key=request.session.session_key)
        else:
            print('cart found for the session but without user')
            cart = cart_session.first()
            cart.user = request.user
            cart.save()
    # If there is already a Cart for current user, check if its 'session_key' is equal to current request.session_key
    else:
        print('user already has a cart')
        cart = cart_qs.first()
    return cart


def get_cart_and_cart_item_id(cart_model: object, cart_id: int, cart_item_id: int) -> tuple():
    """
    Helper function to get correct CartItem. Mainly used in 'Cart.change_item_quantity' and 'Cart.delete_item' methods.
    If properly executed return tuple consists of '(CartItem instance, CartItem.product.product_id)'. Otherwise returns None
    """
    cart = get_cart_with_id(cart_model, cart_id)
    if not cart:
        return None
    # Follow line is more optimal than this: "CartItem.objects.filter()" because 'cart' has fewer cartitem than CartItem
    cartItem_qs = cart.cartitem_cart.filter(id=cart_item_id)
    if not cartItem_qs.exists():
        return None
    cartItem = cartItem_qs.get()
    cartItemProductId = cartItem.product.product_id
    return cartItem, cartItemProductId


def synch_cart_session_cart_after_authentication(_model: object, request: HttpRequest) -> tuple:
    """Helper function. Arguements: _model=Cart, request=HttpRequest.
    After user login or signup, create or get Cart for the user, set 'cart_id' session to current cart
    and synchronize Cart data with session data. Returns a tuple consist of (True, cart)."""
    cart = get_or_create_cart_auth_session_key(_model, request)
    request.session['cart_id'] = cart.id
    result = cart.sync_session_cart_after_authentication(request)
    return result, cart
