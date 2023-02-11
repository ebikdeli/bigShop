"""
We are using this document to get admin reverse urls:
https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#reversing-admin-urls
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# from accounts.models import Address
from accounts.models import Address


User = get_user_model()


class TestUser(TestCase):

    def test_create_user(self):
        """Test if create properly"""
        user = User.objects.create_user(username='ehsan', password='123456')

        self.assertEqual(user.username, 'ehsan')
    
    def test_create_super_user(self):
        """Test create super user"""
        super_user = User.objects.create_superuser('reza')

        self.assertEqual(super_user.username, 'reza')
    
    def test_delete_user(self):
        """Test if user delete properly"""
        user = User.objects.create_user(username='reza', password='123456')
        User.objects.filter(id=user.id).delete()
        try:
            user = User.objects.get(username='reza')
            no_user = user
        except User.DoesNotExist:
            no_user = None

        self.assertIsNone(no_user, 'user is not')
    
    def test_user_login(self):
        """Test if users can login"""
        self.user = User.objects.create_superuser(username='reza', password='1234567')
        is_login = self.client.login(username='reza', password='1234567')
        req = self.client.get(reverse('admin:index'))
            
        self.assertTrue(is_login, 'users could not login')
        self.assertEqual(req.status_code, 200)
    
    def test_user_signals_discount_score(self):
        """Test if discount_score and signals in user work properly"""
        values_kwargs = {'username': 'reza', 'password': '123456', 'score': 1330, 'discount_percent': 92}
        user = User(**values_kwargs, discount_value=20000)
        user.save()
        # print(f"user score: {self.user.score}, user discount value: {self.user.discount_value},\
        #         user lifetime score: {self.user.score_lifetime}, user discount percent: {self.user.discount_percent}")
        self.assertEqual(user.score, 0)
        self.assertEqual(user.discount_value, 40000)
        self.assertEqual(user.score_lifetime, 1330)
        self.assertEqual(user.discount_percent, 92)

        user.score = 782
        user.save()

        self.assertEqual(user.score_lifetime, 1330 + 782)


class TestClient(TestCase):
    def setUp(self) -> None:
        user_data = {'username': 'reza', 'password': '1234567'}
        self.user = get_user_model().objects.create_user(**user_data)
        admin_data = {'username': 'ehsan', 'password': '123456'}
        self.admin = get_user_model().objects.create_superuser(**admin_data)
        self.client = Client()
        # NOTE: get_user_model().objects.create(**user_data) does not hash 'password' unlike the
        # get_user_model().objects.create_user(**user_data). So use the latter

    def test_login_access(self):
        """Test if only authenticated users could access restricted pages"""
        request = self.client.get(reverse('admin:index'))
        # OR: request = self.client.get('/admin/')  <==> It's absolute pass but with 'reverse' we use namespace
        self.assertNotEqual(request.status_code, 200)
        # Now if log user in
        is_login = self.client.login(username='ehsan', password='123456')
        request = self.client.get(reverse('admin:index'))

        self.assertEqual(is_login, True)
        self.assertEqual(request.status_code, 200)

    def test_superuser_access(self):
        """Test if only supserusers access admin page"""
        self.assertIn(get_user_model().objects.get(username='reza'), get_user_model().objects.all())
        # Although 'reza' can login, It cannot access 'django admin' because it's not a super user
        user_is_login = self.client.login(username='reza', password='1234567')
        request = self.client.get(reverse('admin:index'))

        self.assertEqual(user_is_login, True)
        self.assertEqual(request.status_code, 302)

        # Now login with a super user or staff member
        super_is_login = self.client.login(username='ehsan', password='123456')
        request = self.client.get(reverse('admin:index'))

        self.assertEqual(super_is_login, True)
        self.assertEqual(request.status_code, 200)

        # Now we change 'user' to staff member and login again but first we should logout current user
        self.client.logout()
        self.user.is_staff = True
        # self.user.is_admin = True
        # self.user.is_superuser = True
        self.user.save()
        user_is_login = self.client.login(username='reza', password='1234567')
        request = self.client.get(reverse('admin:index'))

        self.assertEqual(user_is_login, True)
        self.assertEqual(request.status_code, 200)


class TestUserAddress(TestCase):
    def setUp(self) -> None:
        data = {'username': 'ehsan', 'password': '123456'}
        self.user = get_user_model().objects.create_superuser(**data)
    
    def test_if_address_created_after_user(self):
        """Test if address created automatically after user"""
        self.assertIn(self.user.address, Address.objects.all())

    def test_create_delete_address(self):
        """Test if Address created and deleted successfully"""
        # First deleted address created automatically
        self.assertIn(self.user.address, Address.objects.all())
        self.user.address.delete()
        self.assertNotIn(self.user.address, Address.objects.all())

        # Now create a new address for the user
        address_data = {'user': self.user, 'state': 'Khoozestan', 'city': 'Ahwaz', 'line': 'Bahonar'}
        # Create Address
        address = Address.objects.create(**address_data)
        self.assertEqual(address.state, 'Khoozestan')

        # Delete Address
        Address.objects.filter(user=self.user).delete()
        self.assertIsNone(Address.objects.filter(state='Khoozestan').first())
