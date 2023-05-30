from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from product.models import Product
from cart.models import Cart, CartItem


class CartViewTest(TestCase):
    """Test Cart views"""
    def setUp(self) -> None:
        self.client = Client(False)
        user_data = {'username': 'ehsan@gmail.com', 'password': '123456'}
        self.user = get_user_model().objects.create(**user_data)
        self.product = Product.objects.create(name='Samsung s21', price=200000, stock=10)
    
    def test_add_to_cart_view(self):
        """Test if add_product_cart view works fine"""
        url = reverse('cart:add-product-cart')
        print(self.product.stock)
        # !! https://stackoverflow.com/questions/42521230/how-to-escape-curly-brackets-in-f-strings
        post_data = {'data': [f'{{"quantity": 4, "product-id": "{self.product.product_id}"}}']}
        response = self.client.post(url, data=post_data)
        print(response.status_code)
        print(response.json())
        self.product.refresh_from_db()
        print(self.product.stock)
