from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from product.models import Product
from cart.models import Cart, CartItem

import uuid


class CartViewTestUnauthenticatedUser(TestCase):
    """Test Cart views for unauthenticated user"""
    def setUp(self) -> None:
        self.client = Client(False)
        self.product = Product.objects.create(name='Samsung s21', price=200000, stock=10)
    
    def test_add_to_cart_view_success(self):
        """Test if add_product_cart view works fine"""
        url = reverse('cart:add-product-cart')
        # print(self.product.stock)
        # !! https://stackoverflow.com/questions/42521230/how-to-escape-curly-brackets-in-f-strings
        post_data = {'data': [f'{{"quantity": 4, "product-id": "{self.product.product_id}"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 201)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertEqual(self.product.stock, 10-4)
    
    def test_add_to_cart_view_failure(self):
        """Test if add_product_cart view failed if there is not enough items in the stock"""
        url = reverse('cart:add-product-cart')
        post_data = {'data': [f'{{"quantity": 11, "product-id": "{self.product.product_id}"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 402)
        self.assertEqual(response.json()['status'], 'nok')
        self.assertEqual(self.product.stock, 10)
    
    def test_change_product_cart_view_success(self):
        """"Test change_product_cart view"""
         # Create a Cart and put a product in the Cart
        cart = Cart.objects.create()
        cart.cart_item_cart.create(product=self.product, quantity=3, price=30000, price_pay=30000)
        print(cart.price, '    ', cart.price_pay)
        url = reverse('cart:change-product-cart')
        post_data = {'data': [f'{{"quantity": 5, "product-id": "{self.product.product_id}", "cart-id": "{cart.id}"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 201)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertEqual(self.product.stock, 10-5)
    
    def test_change_product_cart_view_failure(self):
        """"Test change_product_cart view failed if 'cart-id' is wrong"""
        # Create a Cart and put a product in the Cart
        cart = Cart.objects.create()
        cart.cart_item_cart.create(product=self.product, quantity=3, price=30000, price_pay=30000)
        print(cart.price, '    ', cart.price_pay)
        url = reverse('cart:change-product-cart')
        post_data = {'data': [f'{{"quantity": 5, "product-id": "{self.product.product_id}", "cart-id": "913"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 402)
        self.assertEqual(response.json()['status'], 'nok')
        self.assertEqual(self.product.stock, 10)
    
    def test_delete_item_cart_success(self):
        """Test if an CartItem deleted from the Cart successfully"""
        # Create a cart and put a item int the cart
        cart = Cart.objects.create()
        cart.cart_item_cart.create(product=self.product, quantity=3, price=30000, price_pay=30000)
        # print(cart.price, '    ', cart.price_pay)
        self.assertEqual(cart.quantity, 3)
        self.assertEqual(self.product.stock, 10)
        url = reverse('cart:delete-item-cart')
        post_data = {'data': [f'{{"product-id": "{self.product.product_id}", "cart-id": "{cart.id}"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        cart.refresh_from_db()
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 202)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertEqual(cart.quantity, 3 - 3)
        self.assertEqual(self.product.stock, 10 + 3)
    
    def test_delete_item_cart_failed(self):
        """Test if an CartItem deleted from the Cart unsessful because 'product-id' is not a valid product.id"""
         # Create a cart and put a item int the cart
        cart = Cart.objects.create()
        cart.cart_item_cart.create(product=self.product, quantity=3, price=30000, price_pay=30000)
        # print(cart.price, '    ', cart.price_pay)
        self.assertEqual(cart.quantity, 3)
        self.assertEqual(self.product.stock, 10)
        url = reverse('cart:delete-item-cart')
        post_data = {'data': [f'{{"product-id": "{uuid.uuid4()}", "cart-id": "{cart.id}"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        cart.refresh_from_db()
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 402)
        self.assertEqual(response.json()['status'], 'nok')
        self.assertEqual(cart.quantity, 3 - 0)
        self.assertEqual(self.product.stock, 10 + 0)


class CartViewTestAuthenticatedUser(TestCase):
    """Test Cart views for authenticated user"""
    def setUp(self) -> None:
        self.client = Client(False)
        self.user_data = {'username': 'ehsan@gmail.com', 'password': '123456'}
        self.user = get_user_model().objects.create(**self.user_data)
        self.product = Product.objects.create(name='Samsung s21', price=200000, stock=10)
    
    def test_add_to_cart_view_success(self):
        """Test if authenticated user can add item to its cart"""
        is_login = self.client.force_login(self.user)
        self.assertIs(is_login, None)
        url = reverse('cart:add-product-cart')
        # !! https://stackoverflow.com/questions/42521230/how-to-escape-curly-brackets-in-f-strings
        post_data = {'data': [f'{{"quantity": 4, "product-id": "{self.product.product_id}"}}']}
        response = self.client.post(url, data=post_data)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 201)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertEqual(self.product.stock, 10-4)
