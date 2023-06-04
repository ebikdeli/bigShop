from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestLoginViews(TestCase):
    """Test login app views"""
    def setUp(self) -> None:
        self.client = Client(enforce_csrf_checks=False)
        self.user_data = {'username': 'ehsan@gmail.com', 'password': '123456'}
        self.user = get_user_model().objects.create_user(**self.user_data)
    
    def test_classic_login_view_success(self):
        """Test if classic login view works properly"""
        url = reverse('login:classic-login')
        # !! https://stackoverflow.com/questions/42521230/how-to-escape-curly-brackets-in-f-strings
        post_data = {'data': [f'{{"username": "{self.user_data["username"]}", "password": "{self.user_data["password"]}"}}']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 200)
    
    def test_classic_login_view_failed(self):
        """Test if classic login view returns error because of wrong username or password"""
        url = reverse('login:classic-login')
        # !! https://stackoverflow.com/questions/42521230/how-to-escape-curly-brackets-in-f-strings
        post_data = {'data': [f'{{"username": "wrong@fake.com", "password": "123456"}}']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 401)
    
    def test_sign_up_view_success(self):
        """Test if sign up view works properly"""
        url = reverse('login:signup')
        post_data = {'data': [f'{{"username": "09351112233", "password": "123456"}}']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 201)
    
    def test_sign_up_view_failed(self):
        """Test if sign up view failed because the username is already registered"""
        url = reverse('login:signup')
        post_data = {'data': [f'{{"username": "ehsan@gmail.com", "password": "123456"}}']}
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 400)
