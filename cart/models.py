from django.db import models
from django.db.models import Sum
from django.http.request import HttpRequest
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from product.models import Product, Color, ColorPrice
from .cart_functions import reset_session, set_session_cart, get_cart_with_id,\
                            get_cart_and_cart_item_id


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
        return int(self.cart_item_cart.aggregate(price=Sum('price'))['price'])
    
    @property
    def price_pay(self):
        """Calculate total price_pay of the current cart"""
        if not self.cart_item_cart.exists():
            return 0
        # Following code is the most brief code to calcualte price_pay of all CartItem of the current Cart
        return int(self.cart_item_cart.aggregate(price_pay=Sum('price_pay'))['price_pay'])
    
    @property
    def quantity(self):
        """Calculate total items in the current cart"""
        if not self.cart_item_cart.exists():
            return 0
        # Following code is the most brief code to calcualte price_pay of all CartItem of the current Cart
        return int(self.cart_item_cart.aggregate(quantity=Sum('quantity'))['quantity'])
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug and self.user:
            self.slug = slugify(f'{self.user.username}_cart')
        elif not self.slug and not self.user:
            self.slug = f'cart({self.id})'
        return super().save(*args, **kwargs)
    
    def append_item(self, request: HttpRequest, quantity: (str or int), product_id: str, color_name: str, *args, **kwargs) -> bool:
        """Append new items to the current cart by creating new CartItem if not exists.
        If 'product.stock' is less than the 'quantity' selected by customer, stop the operation
        and returns False"""
        cart = self
        cartItem = None
        product = Product.objects.get(product_id=product_id)
        cartItem_qs = cart.cart_item_cart.filter(product=product)
        # If item is already in the user cart
        if cartItem_qs.exists():
            print(f'{product.name} already exists in the cart just update it')
            cartItem = cartItem_qs.get()
            # If there is not enough items in the Product.stock, stop operation
            if product.stock < int(quantity):
                print('Not enough product in the stock')
                return False
            product.stock -= int(quantity)
            product.save()
            product.refresh_from_db()
            cartItem.quantity += int(quantity)
            cartItem.save()
            # Update 'cart' session with new quantity
            for item in request.session['cart']:
                if item['product_id'] == product_id:
                    item['quantity'] += int(quantity)
                    if color_name:
                        item['color': color_name]
        # If the item is not in the cart before
        else:
            if product.stock < int(quantity):
                print('Not enough product in the stock')
                return False
            product.stock -= int(quantity)
            product.save()
            product.refresh_from_db()
            cartItem = cart.cart_item_cart.create(product=product, quantity=int(quantity))
            print('New cart item created')
            # Update 'cart' session with new quantity
            new_item_data = {'product_id': str(product.product_id), 'quantity': int(quantity)}
            if color_name:
                new_item_data.update({'color': color_name})
            request.session['cart'].append(new_item_data)
        # Update session with updated Cart
        set_session_cart(request, cartItem.cart)
        return True


    def change_item_quantity(self, quantity: (str or int), request: HttpRequest,
                                   cart_item_id: int=None, *args, **kwargs) -> bool:
        """Change the quantity of an item by its 'cart_item_id' field. At least one of the 'cart_item_id'
        or 'product_id' arguements must be true. If successfully done returns True othrewise returns False."""
        cartItem_qs = self.cart_item_cart.filter(id=cart_item_id)
        if not cartItem_qs.exists():
            return False
        cartItem = cartItem_qs.get()
        product = cartItem.product
        # If there is not enough items in the Product.stock, stop the operation
        if product.stock < int(quantity):
            return False
        # Subtract number of added item from product stock
        product.stock -= int(quantity)
        product.save()
        cartItem.quantity = int(quantity)
        cartItem.save()
        # Update 'cart' session with new quantity
        for item in request.session['cart']:
            if item['product_id'] == product.product_id:
                item['quantity'] = int(quantity)
        # Update session with updated Cart
        set_session_cart(request, cartItem.cart)
        return True


    def delete_item(self, request: HttpRequest, cart_item_id: int, *args, **kwargs) -> bool:
        """Delete an item from the cart by its 'CartItem.id'. If properly executed returns True else False.
        Oprional: We can add the functionality that be able to delete an item with 'Product.product_id' field."""
        cartItem_qs = self.cart_item_cart.filter(id=cart_item_id)
        if not cartItem_qs.exists():
            return None
        cartItem = cartItem_qs.get()
        product = cartItem.product
        # Add the current 'CartItem.quantity' to 'product.stock' before being deleted
        product.stock += int(cartItem.quantity)
        product.save()
        cartItem.delete()
        # Delete current item from 'cart' session
        for item in request.session['cart']:
            if item['product_id'] == product.product_id:
                request.session['cart'].remove(item)
        # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
        set_session_cart(request, cartItem.cart)
        return True
        

    def clean(self, request: HttpRequest, **kwargs) -> bool:
        """Clean the cart and delete all items in it and reset cart sessions. If delete was a success
        returns True otherwise return False"""
        # Reset all cart sessions
        reset_session(request)
        cart = self
        if not cart:
            return None
        cartItems = cart.cart_item_cart.all()
        if not cartItems.exists():
            print('Cart is already clean!')
            return True
        for cI in cartItems:
            # Add back CartItem.quantity to the 'product.stock' before deleting the CartItem
            cI.product.stock += int(cI.quantity)
            cI.product.save()
            cI.delete()
        print('Everything deleted from the cart and Cart is clean')
        return True

    
    def sync_session_cart_after_authentication(self, request: HttpRequest, *args, **kwargs):
        """Synchronize Cart and cart session after user authenticated."""
        cart = self
        # Fetch all CartItem of the current Cart
        cartItems = cart.cart_item_cart.all()
        # 1) If cart session is not empty, put its items in the Cart
        try:
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
                        for item in request.session['cart']:
                            # Add every item['product_id'] to a list to be used in '1.3' step
                            current_cart_product_id = list()
                            current_cart_product_id.append(item['product_id'])
                            # 1.1- If the session item is already in the CartItem, just add quantity to the current CartItem
                            if cI.product.product_id == item['product_id']:
                                cI.quantity += int(item['quantity'])
                                print(f"{item['product_id']} is already in the cart and updated")
                                cI.save()
                                item['quantity'] = cI.quantity
                            # 1.2- If the session item is not in the CartItem, add new CartItem to the Cart
                            elif item['product_id'] not in productId:
                                cart.cart_item_cart.create(
                                    product=Product.objects.get(product_id=item['product_id']),
                                    quantity=int(item['quantity'])
                                )
                                # Append current 'product_id' to 'productId' list to prevent duplication
                                productId.append(item['product_id'])
                                print(f"{item['product_id']} was not in the cart but added")
                        # 1.3- If the current CartItem is not in the 'cart' session, add it to the session
                        if str(cI.product.product_id) not in current_cart_product_id:
                            # Later we can add ColorPrice functionality to this section
                            request.session['cart'].append({'product_id': cI.product.product_id, 'quantity': int(cI.quantity)})
                # 2- If current Cart is empty (or there is no CartItem) just put all items from cart sesison in the Cart
                else:
                    for item in request.session['cart']:
                        cart.cartitem_cart.create(
                            product=Product.objects.get(product_id=item['product_id']),
                            quantity = int(item['quantity'])
                        )
            # 2) If cart session is empty, check if there is any item in Cart to put them into the empty session
            else:
                if cartItems:
                    for cI in cartItems:
                        request.session['cart'].append({'product_id': cI.product.product_id, 'quantity': int(cI.quantity)})
                # If both the Cart and cart session are empty, just return None
                else:
                    return None
            # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
            set_session_cart(request, cart)
            return True
        except KeyError:
            print('No cart_id found in session so no synchnorization happened')
            return False


class CartItem(models.Model):
    """Any item added to cart, represented in this model"""
    cart = models.ForeignKey('Cart',
                             verbose_name=_('cart'),
                             on_delete=models.CASCADE,
                             related_name='cart_item_cart')
    product = models.ForeignKey('product.Product',
                                verbose_name=_('product'),
                                on_delete=models.CASCADE,
                                related_name='cart_item_product')
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
