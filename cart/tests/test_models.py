from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Cart, CartItem
from shop.models import Product


class TestCart(TestCase):
    """Test Cart methods"""
    def setUp(self) -> None:
        user_data = {'username': 'green_apple@gmail.com', 'password': '12345'}
        self.user = get_user_model().objects.create_superuser(**user_data)
        self.product_laptop = Product.objects.create(name='laptop', price=10000, stock=10, is_available=True)
        self.product_phone = Product.objects.create(name='phone', price=8000, stock=15, is_available=True)
    
    def test_create_anynomous_cart(self):
        """Test if we can create anynomous cart"""
        cart = Cart.objects.create(price=10000)
        self.assertIn(cart, Cart.objects.all())
        self.assertIsNone(cart.user)
    
    def test_cart_create(self):
        """Test create cart"""
        cart = Cart.objects.create(user=self.user, price=20000)
        self.assertEqual(cart.user, self.user)
        self.assertIsNotNone(cart.user)
    
    def test_cart_update(self):
        """Test delete cart"""
        cart = Cart.objects.create(user=self.user, price=20000)
        self.assertEqual(cart.price, 20000)

        cart.price = 14000
        cart.save()
        self.assertEqual(cart.price, 14000)
    
    def test_cart_delete(self):
        """Test if cart deleted properly"""
        cart = Cart.objects.create(user=self.user, price=20000)
        self.assertIn(cart, Cart.objects.all())

        cart.delete()
        self.assertNotIn(cart, Cart.objects.all())
    
    def test_user_create_carts(self):
        """Test if user can create carts"""
        self.assertNotIn(self.user.cart_user.all(), Cart.objects.all())
        cartCheap = self.user.cart_user.create(price=2000)
        cartExpensive = self.user.cart_user.create(price=60000)

        self.assertEqual(cartCheap.user, self.user)
        self.assertEqual(cartExpensive.user, self.user)
        self.assertIn(cartCheap, Cart.objects.all())
    
    def test_user_update_delete_cart(self):
        """Test if user can update and delete carts"""
        cartCheap = self.user.cart_user.create(price=2000)
        cartExpensive = self.user.cart_user.create(price=60000)
        self.assertIn(cartCheap, Cart.objects.all())
        self.assertIn(cartExpensive, Cart.objects.all())

        cart = self.user.cart_user.filter(price__gt=30000).get()
        self.assertIn(cart, Cart.objects.all())
        self.assertEqual(cart.price, 60000)

        cart.price = 40000
        cart.save()
        self.assertEqual(cart.price, 40000)

        self.user.cart_user.filter(price__lte=40000).delete()
        self.assertNotIn(cartCheap, Cart.objects.all())
        self.assertNotIn(cartExpensive, Cart.objects.all())
    
    def test_cart_field_quantity_and_price_and_price_end_on_item_cart_quantity(self):
        """Test if we can calculate 'quantity', 'price', and 'price_end' fields for the cart based on the
        'cart_item' field on CartItem"""
        cart = Cart.objects.create()
        # Create some numbers of "CartItem"s with arbitrary number of 'quantity'
        cart.cartitem_cart.create(product=self.product_laptop, quantity=3)
        cart.cartitem_cart.create(product=self.product_phone, quantity=9)
        CartItem.objects.create(cart=cart, product=self.product_laptop, quantity=4)
        cart.save()
        self.assertEqual(cart.total_quantity, 16)
        self.assertEqual(cart.price, 142000)
        self.assertEqual(cart.price_end, 142000)


class TestCartItem(TestCase):
    """Test CartItem methods"""
    def setUp(self) -> None:
        # We can Import all attributes from 'TestCart' class by following line
        # TestCart.setUp(self)
        user_data = {'username': 'green_apple@gmail.com', 'password': '12345'}
        self.user = get_user_model().objects.create_superuser(**user_data)
        self.product_laptop = Product.objects.create(name='laptop', price=1000, stock=10)
        self.product_phone = Product.objects.create(name='phone', price=700, stock=15)
        self.cart = Cart.objects.create()
    
    def test_create_cart_item(self):
        """Test if cart item created successfully"""
        cartItemLaptopData = {'cart': self.cart,
                              'product': self.product_laptop,
                              'price': self.product_laptop.price, 
                              'price_end': self.product_laptop.price}
        cart_item_laptop = CartItem.objects.create(**cartItemLaptopData)
        self.assertIn(cart_item_laptop, CartItem.objects.all())

    def test_update_cart_item(self):
        """Test if cart item updated successfully"""
        cartItemLaptopData = {'cart': self.cart,
                              'product': self.product_laptop,
                              'price': self.product_laptop.price, 
                              'price_end': self.product_laptop.price}
        cart_item_laptop = CartItem.objects.create(**cartItemLaptopData)
        self.assertEqual(cart_item_laptop.product.stock, 10)
        self.assertEqual(cart_item_laptop.quantity, 1)

        cart_item_laptop.quantity = 3
        cart_item_laptop.save()
        self.assertEqual(cart_item_laptop.quantity, 3)
    
    def test_delete_cart_item(self):
        """Test if cart item deleted successfully"""
        cartItemLaptopData = {'cart': self.cart,
                              'product': self.product_laptop,
                              'price': self.product_laptop.price, 
                              'price_end': self.product_laptop.price}
        cart_item_laptop = CartItem.objects.create(**cartItemLaptopData)
        self.assertIn(cart_item_laptop, CartItem.objects.all())

        cart_item_laptop.delete()
        self.assertNotIn(cart_item_laptop, CartItem.objects.all())
    
    def test_get_and_update_user_from_cart_item(self):
        """Test if we can get and update user from cart item"""
        cartItemLaptopData = {'cart': self.cart,
                              'product': self.product_laptop,
                              'price': self.product_laptop.price, 
                              'price_end': self.product_laptop.price}
        cart_item_laptop = CartItem.objects.create(**cartItemLaptopData)

        self.assertNotEqual(cart_item_laptop.cart.user, self.user)

        cart_item_laptop.cart.user = self.user
        cart_item_laptop.cart.save()
        self.assertEqual(cart_item_laptop.cart.user, self.user)
    
    def test_subtract_cart_quantity_from_cart_total_quantity_before_deletation(self):
        """Test if by delete the 'cart_item', 'total_quantity' of the parent 'cart' subtracted
        by 'cart_item.quantity'"""
        cartItemLaptopData = {'cart': self.cart,
                              'product': self.product_laptop,
                              'quantity': 5}
        cart_item_laptop = CartItem.objects.create(**cartItemLaptopData)
        self.assertIn(cart_item_laptop, CartItem.objects.all())
        self.assertEqual(cart_item_laptop.quantity, 5)
        
        initial_quantity = self.cart.total_quantity = 12
        self.cart.save()
        self.assertEqual(self.cart.total_quantity, 12)

        cart_item_laptop.delete()
        self.assertNotIn(cart_item_laptop, CartItem.objects.all())
        self.assertEqual(self.cart.total_quantity, (initial_quantity - cart_item_laptop.quantity))

    def test_substract_cart_item_price_and_price_end_from_cart_before_deletation(self):
        """Test if by delete the 'cart_item', 'price' and 'price_end' fields of the parent 'cart' substracted properly"""
        cart_item_laptop = CartItem.objects.create(cart=self.cart, product=self.product_laptop, quantity=8)
        cart_item_phone = CartItem.objects.create(cart=self.cart, product=self.product_phone, quantity=6)

        self.assertEqual(self.cart.total_quantity, 14)
        self.assertEqual(self.cart.price, cart_item_laptop.price + cart_item_phone.price)
        self.assertEqual(self.cart.price_end, cart_item_laptop.price_end + cart_item_phone.price_end)

        cart_item_phone.delete()
        self.assertEqual(self.cart.total_quantity, 8)
        self.assertEqual(self.cart.price, cart_item_laptop.price)
        self.assertEqual(self.cart.price_end, cart_item_laptop.price_end)
    
    def test_calculate_item_cart_price_and_price_end(self):
        """Test if 'price' and 'price_end' fields calculated properly for the itemcart"""
        cartItemLaptopData = {'cart': self.cart,
                              'product': self.product_laptop,
                              'quantity': 5}
        cart_item_laptop = CartItem.objects.create(**cartItemLaptopData)
        self.assertEqual(cart_item_laptop.price, self.product_laptop.price * 5)
        self.assertEqual(cart_item_laptop.price_end, self.product_laptop.price_end * 5)


class TestCartObjectsMethods(TestCase):
    """Test Cart object methods"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username='green_apple@gmail.com', password='123456')
        self.product_laptop = Product.objects.create(name='laptop', price=1000, stock=10)
        self.product_phone = Product.objects.create(name='phone', price=700, stock=15)
        self.cart = Cart.objects.create()
        self.cartitem_laptop = CartItem.objects.create(
            cart=self.cart,
            product=self.product_laptop,
            quantity=3
        )
        self.cartitem_phone = CartItem.objects.create(
            cart=self.cart,
            product=self.product_phone,
            quantity=2
        )
    
    def setup_client_request_session(self):
        """Setup client and simulate request object and session and return a tuple with this elements:
        (result: bool, request: WSGIRequest, client: Client)."""
        client = Client()
        response = client.get(reverse('shop:shop'))
        request = response.wsgi_request
        request.session['cart'] = dict()
        request.session['total_quantity'] = 0
        request.session['price'] = 0
        request.session['price_end'] = 0
        result = self.cart.sync_session_cart_after_authentication(request)
        # print(self.cart.total_quantity, '       ', self.cart.price)
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
        # self.assertTrue(result)
        return result, request, client
    
    def test_sync_nonempty_cart_session_empty_cart(self):
        """Test if empty Cart would be filled by nonempty session"""
        # Delete all items in Cart
        self.assertEqual(self.cart.total_quantity, 5)
        self.assertIn(self.cartitem_laptop, self.cart.cartitem_cart.all())
        # To delete objects in a queryset, we should not delete it directly: self.cart.cartitem_cart.all().delete()
        for cartitem in self.cart.cartitem_cart.all():
            cartitem.delete()
        self.assertNotIn(self.cartitem_laptop, self.cart.cartitem_cart.all())
        self.assertEqual(self.cart.total_quantity, 0)

        # This is how we simulate a request object with its session
        client = Client()
        # Note: We don't really have to use a sprecific 'url' to create a response object needed to create a request
        # object. It's only need to be a correct 'url' or 'view' and does not have any dependency to session
        response = client.get(reverse('shop:shop'))
        request = response.wsgi_request
        request.session['cart'] = {self.product_laptop.product_id: 3}
        request.session['total_quantity'] = 3
        request.session['price'] = 3000
        request.session['price_end'] = 300
        result = self.cart.sync_session_cart_after_authentication(request)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_quantity, 3)
        self.assertTrue(result)
    
    def test_sync_empty_cart_session_nonempty_cart(self):
        """Test if we can fill empty cart session with nonempty Cart"""
        # Check if Cart is non empty
        self.assertEqual(self.cart.total_quantity, 5)

        result, request, client = self.setup_client_request_session()
        self.assertEqual(request.session['total_quantity'], 5)
        self.assertEqual(self.cart.total_quantity, 5)
        self.assertTrue(result)
    
    def test_sync_empty_cart_session_empty_cart(self):
        """Test if empty session and empty Cart return False"""
        self.assertEqual(self.cart.total_quantity, 5)
        for cartitem in self.cart.cartitem_cart.all():
            cartitem.delete()
        self.assertEqual(self.cart.total_quantity, 0)

        result, request, client = self.setup_client_request_session()
        self.assertEqual(request.session['total_quantity'], 0)
        self.assertEqual(self.cart.total_quantity, 0)
        self.assertFalse(result)

    def test_sync_nonempty_session_cart_nonempty_cart(self):
        """Test if syncing non empty cart session and non empty Cart works properly"""
        # This is how we simulate a request object with its needed session
        client = Client()
        response = client.get(reverse('shop:shop'))
        request = response.wsgi_request
        # request.session['cart'] = {self.product_laptop.product_id: 1}
        request.session['cart'] = {self.product_laptop.product_id: 5, self.product_phone.product_id: 3}
        # iwatch_product = Product.objects.create(name='iwatch', stock=20, price=500, price_end=400)
        # request.session['cart'].update({iwatch_product.product_id: 3})
        request.session['total_quantity'] = 3
        request.session['price'] = 1000
        request.session['price_end'] = 900
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
        # print(self.cart.total_quantity, '    ', self.cart.price, '    ', self.cart.price_end)
        result = self.cart.sync_session_cart_after_authentication(request)
        self.cart.refresh_from_db()
        # print(self.cart.total_quantity, '    ', self.cart.price, '    ', self.cart.price_end)
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
    
    def test_clean_cart_session(self):
        """Test if Cart cleaned successfully"""
        result, request, client = self.setup_client_request_session()

        is_cleaned = Cart.objects.clean(self.cart.id, request)
        self.cart.refresh_from_db()
        # print(self.cart.total_quantity, '       ', self.cart.price)
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
        self.assertTrue(is_cleaned)
    
    def test_delete_from_cart_session(self):
        """Test if deleting a product from the Cart is properly implemented"""
        result, request, client = self.setup_client_request_session()

        res = self.cart.sync_session_cart_after_authentication(request)
        # print(self.cart.total_quantity, '       ', self.cart.price)
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
        self.assertTrue(res)
    
    def test_change_item_quantity(self):
        """Test if changing item quantity is successful using CartManager.change_item_quantity"""
        client = Client()
        response = client.get(reverse('shop:shop'))
        request = response.wsgi_request
        request.session['cart'] = dict()
        request.session['total_quantity'] = 0
        request.session['price'] = 0
        request.session['price_end'] = 0
        result = self.cart.sync_session_cart_after_authentication(request)
        # print(self.cart.total_quantity, '       ', self.cart.price)
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
        self.assertTrue(result)

        res = Cart.objects.change_item_quantity(10, self.cart.id, request, self.cartitem_laptop.id)
        self.cart.refresh_from_db()
        # print(self.cart.total_quantity, '       ', self.cart.price)
        # print(request.session['cart'], '   ', request.session['total_quantity'], '    ', request.session['price'], '    ', request.session['price_end'])
        self.assertTrue(res)
