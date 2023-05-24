from django.test import TestCase
from django.contrib.auth import get_user_model

from cart.models import Cart
from product.models import Product, Color, ColorPrice
from .models import Order, OrderItem


class OrderTest(TestCase):
    def setUp(self) -> None:
        username_data = {'username': 'ehsan@gmail.com', 'password': '12345'}
        self.user = get_user_model().objects.create(**username_data)
        self.cart = Cart.objects.create(user=self.user)
        self.order = Order.objects.create(cart=self.cart)
    
    def test_order_exist(self):
        """Test if order model works"""
        self.assertIn(self.order, Order.objects.all())
    
    def test_order_price_(self):
        """Test if order price is zero"""
        self.assertEqual(self.order.price(), 0)
    

class OrderItemTest(TestCase):
    def setUp(self) -> None:
        username_data = {'username': 'ehsan@gmail.com', 'password': '12345'}
        self.user = get_user_model().objects.create(**username_data)
        self.product = Product.objects.create(name='Samsung laptop', price=2500000)
        self.cart = Cart.objects.create(user=self.user)
        self.order = Order.objects.create(cart=self.cart)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=3)
        self.color_red = Color.objects.create(name='red')
        self.color_blue = Color.objects.create(name='blue')
    
    def test_order_items_exists(self):
        """Test Order items"""
        self.assertIn(self.order_item, OrderItem.objects.all())
    
    def test_order_item_price(self):
        """Test if OrderItem price() works"""
        self.assertEqual(int(self.product.price * 3), self.order_item.price())
    
    def test_order_items_price_paid(self):
        """Test if OrderItem price_pay() works"""
        self.product.discount = 500
        self.product.save()
        self.assertEqual(int((self.product.price - self.product.discount) * 3), self.order_item.price_pay())
    
    def test_order_items_price_paid(self):
        """Test ColorPrice price gap"""
        cp_red = ColorPrice.objects.create(product=self.product, color=self.color_red)
        cp_blue = ColorPrice.objects.create(product=self.product, color=self.color_blue, extra_price=800)
        oi_blue = OrderItem.objects.create(order=self.order, product=self.product, color=self.color_blue, quantity=3)
        oi_red = OrderItem.objects.create(order=self.order, product=self.product, color=self.color_red, quantity=3)

        self.assertEqual(oi_red.price(), self.order_item.price())
        self.assertNotEqual(oi_blue.price(), self.order_item.price())
        self.assertEqual(oi_blue.price(), oi_red.price() + 800 * 3)
