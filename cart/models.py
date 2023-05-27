from django.db import models
from django.db.models import Sum
from django.http.request import HttpRequest
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from product.models import Product
from .cart_functions import reset_session, set_session_cart, get_cart_with_id,\
                            get_cart_and_cart_item_id


class CartManager(models.Manager):
    """Customized manager to add functionality to the Cart manager"""
    def append_item(self, quantity: (str or int), cart_id: int, request: HttpRequest, product_id: str, *args, **kwargs) -> bool:
        """Append new items to the Cart by creating new CartItem if not exists"""
        cartItem = None
        cart = get_cart_with_id(self.model, cart_id)
        product = Product.objects.get(product_id=product_id)
        cartItem_qs = cart.cartitem_cart.filter(product=product)
        if cartItem_qs.exists():
            print(f'{product.name} already exists in the cart just update it')
            cartItem = cartItem_qs.get()
            cartItem.quantity += int(quantity)
            cartItem.save()
            # Update 'cart' session with new quantity
            request.session['cart'][product_id] += int(quantity)
        else:
            print('New cart item created')
            cartItem = cart.cartitem_cart.create(product=product, quantity=int(quantity))
            # Update 'cart' session with new quantity
            request.session['cart'].update({product_id: int(quantity)})
        # Update session with updated Cart
        set_session_cart(request, cartItem.cart)
        return True


    def change_item_quantity(self, quantity: (str or int), cart_id: int, request: HttpRequest,
                                   cart_item_id: int=None, product_id: str=None, *args, **kwargs) -> bool:
        """Change the quantity of an item by its 'cart_item_id' and 'cart_id' fields. At least one of the 'cart_item_id'
        or 'product_id' arguements must be true. If successfully done returns True othrewise returns False."""
        if cart_item_id:
            cartItem, cartItemProductId = get_cart_and_cart_item_id(self.model, cart_id, cart_item_id)
        # If there is no 'cart_item_id', try to get the CartItem with 'Product.product_id'.
        elif product_id:
            cart = get_cart_with_id(self.model, cart_id)
            product = Product.objects.get(product_id=product_id)
            cartItem_qs = cart.cartitem_cart.filter(product=product)
            if not cartItem_qs.exists():
                print('Item does not exist with the product_id code')
                return None
            cartItem = cartItem_qs.get()
            cartItemProductId = cartItem.quantity
        cartItem.quantity = int(quantity)
        cartItem.save()
        # Update 'cart' session with new quantity
        request.session['cart'][str(cartItem.product.product_id)] = int(quantity)
        # Update session with updated Cart
        set_session_cart(request, cartItem.cart)
        return True


    def delete_item(self, cart_id: int, request: HttpRequest, cart_item_id: int, *args, **kwargs) -> bool:
        """Delete an item from the cart by its 'CartItem.id'. If properly executed returns True else False.
        Oprional: We can add the functionality that be able to delete an item with 'Product.product_id' field."""
        cartItem, cartItemProductId = get_cart_and_cart_item_id(self.model, cart_id, cart_item_id)
        cartItem.delete()
        # Delete the product_id from 'cart' session
        r = request.session['cart'].pop(str(cartItemProductId))
        # print('deleted item: ', cartItemProductId, '      ', r)
        # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
        set_session_cart(request, cartItem.cart)
        return True
        

    def clean(self, cart_id: int, request: HttpRequest, **kwargs) -> bool:
        """Clean the cart and delete all items in it and reset cart sessions. If delete was a success
        returns True otherwise return False"""
        # Reset all cart sessions
        reset_session(request)
        cart = get_cart_with_id(self.model, cart_id)
        if not cart:
            return None
        cartItems = cart.cartitem_cart.all()
        if not cartItems.exists():
            print('Cart is already clean!')
            return True
        for cI in cartItems:
            cI.delete()
        print('Everything deleted from the cart and Cart is clean')
        return True


class Cart(models.Model):
    """Any user (even unauthenticated ones) has a cart that works with 'cart' session."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE,
                             related_name='cart_user',
                             blank=True,
                             null=True)
    session_key = models.CharField(verbose_name=_('session key'), blank=True, max_length=30)
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __str__(self) -> str:
        if self.user:
            return f'{self.user.username}_Cart({self.id})'
        return f'Cart({self.id})'
    
    @property
    def price(self):
        """Calculate total price of the current cart"""
        if not self.cart_item_cart.exists():
            return 0
        # Following code is the most brief code to calcualte price of all CartItem of the current Cart
        return int(self.cartitem_cart.aggregate(price=Sum('price'))['price'])
    
    @property
    def price_pay(self):
        """Calculate total price_pay of the current cart"""
        if not self.cart_item_cart.exists():
            return 0
        # Following code is the most brief code to calcualte price_pay of all CartItem of the current Cart
        return int(self.cartitem_cart.aggregate(price_pay=Sum('price_pay'))['price_pay'])
    
    @property
    def quantity(self):
        """Calculate total items in the current cart"""
        if not self.cart_item_cart.exists():
            return 0
        # Following code is the most brief code to calcualte price_pay of all CartItem of the current Cart
        return int(self.cartitem_cart.aggregate(quantity=Sum('quantity'))['quantity'])
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug and self.user:
            self.slug = slugify(f'{self.user.username}_cart')
        elif not self.slug and not self.user:
            self.slug = f'cart({self.id})'
        return super().save(*args, **kwargs)
    
    def sync_session_cart_after_authentication(self, request: HttpRequest, *args, **kwargs):
        """Synchronize Cart and cart session after user authenticated."""
        cart = self
        # Fetch all CartItem of the current Cart
        cartItems = cart.cartitem_cart.all()
        # 1) If cart session is not empty, put its items in the Cart
        if request.session['cart']:
            # 1- If there are CartItems for current Cart (or Cart is not empty)
            if cartItems:
                # First we need to list all current CartItems 'product.product_id' field to know what 'product_id's are
                # already in the 'cart' session to prevent duplication.
                productId = list()
                for cI in cartItems:
                    productId.append(str(cI.product.product_id))
                
                # Check If the item in the 'cart' session is same as any item in the CartItem
                for cI in cartItems:
                    for product_id, quantity in request.session['cart'].items():
                        # 1.1- If the session item is already in the CartItem, just add quantity to the current CartItem
                        if product_id == str(cI.product.product_id):
                            cI.quantity += quantity
                            print(f'{product_id} is already in the cart and updated')
                            cI.save()
                            request.session['cart'][product_id] = cI.quantity
                        # 1.2- If the session item is not in the CartItem, add new CartItem to the Cart
                        elif product_id not in productId:
                            cart.cartitem_cart.create(
                                product=Product.objects.get(product_id=product_id),
                                quantity=quantity
                            )
                            # Append current 'product_id' to 'productId' list to prevent duplication
                            productId.append(product_id)
                            print(f'{product_id} was not in the cart but added')
                    # 1.3- If the current CartItem is not in the 'cart' session, add it to the session
                    if str(cI.product.product_id) not in request.session['cart'].keys():
                        request.session['cart'][str(cI.product.product_id)] = cI.quantity
            # 2- If current Cart is empty (or there is no CartItem) just put all items from cart sesison in the Cart
            else:
                for product_id, quantity in request.session['cart'].items():
                    cart.cartitem_cart.create(
                        product=Product.objects.get(product_id=product_id),
                        quantity = quantity
                    )
        # 2) If cart session is empty, check if there is any item in Cart to put them into the empty session
        else:
            if cartItems:
                for cI in cartItems:
                    request.session['cart'].update({str(cI.product.product_id): cI.quantity})
            # If both the Cart and cart session are empty, just return None
            else:
                return None
        # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
        set_session_cart(request, cart)
        return True


class CartItem(models.Model):
    """Any item added to cart, represented in this model"""
    cart = models.ForeignKey('Cart',
                             verbose_name=_('cart'),
                             on_delete=models.CASCADE,
                             related_name='cart_item_cart')
    product = models.ForeignKey('product.Product',
                                verbose_name=_('product'),
                                on_delete=models.CASCADE,
                                related_name='cartitem_product')
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=1)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=0, default=0)
    price_pay = models.DecimalField(verbose_name=_('price_pay'), max_digits=10, decimal_places=0, default=0)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    _quantity = None

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Item'
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._quantity = self.quantity
    
    def __str__(self) -> str:
        return f'cart({self.cart.id})_product({self.product.name})'
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(f'item {self.product.name}')
        return super().save(*args, **kwargs)
    
    def delete(self, using=None, keep_parents=None):
        """When item deleted from the cart, add quantity to the parent 'product.stock'"""
        self.product.stock += self.quantity
        self.product.save()
        return super().delete(using, keep_parents)
