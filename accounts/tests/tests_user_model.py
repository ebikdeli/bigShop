from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class TestUser(TestCase):

    def test_create_user(self):
        """Test if create properly"""
        user = User.objects.create_user(username='e@gmail.com', password='123456')
        self.assertEqual(user.username, 'e@gmail.com')
    
    def test_create_super_user(self):
        """Test create super user"""
        super_user = User.objects.create_superuser(username='a@gmail.com')

        self.assertEqual(super_user.username, 'a@gmail.com')
    
    def test_delete_user(self):
        """Test if user delete properly"""
        user = User.objects.create_user(username='e@gmail.com', password='123456')
        # User.objects.filter(username=user.username).delete()
        User.objects.filter(id=user.id).delete()
        try:
            user = User.objects.get(username='e@gmail.com')
            no_user = user
        except User.DoesNotExist:
            no_user = None

        self.assertIsNone(no_user, 'user is not')
    
    def test_user_login(self):
        """Test if users can login"""
        self.user = User.objects.create_superuser(username='ehsan@gmail.com', password='1234567')
        is_login = self.client.login(username='ehsan@gmail.com', password='1234567')
        req = self.client.get(reverse('admin:index'))
            
        self.assertTrue(is_login, 'users could not login')
        self.assertEqual(req.status_code, 200)
    
    def test_user_signals_discount_score(self):
        """Test if discount_score and signals in user work properly"""
        self.user = User.objects.create(username='ehsan@gmail.com', password='123456', score=1330, discount_percent=92)
        # print(f"user score: {self.user.score}, user discount value: {self.user.discount_value},\
        #         user lifetime score: {self.user.score_lifetime}, user discount percent: {self.user.discount_percent}")
        
        self.assertEqual(self.user.score, 0)
        self.assertEqual(self.user.discount_value, 20000)
        self.assertEqual(self.user.score_lifetime, 1330)
        self.assertEqual(self.user.discount_percent, 92)

        self.user.score = 782
        self.user.save()

        self.assertEqual(self.user.score_lifetime, 1330 + 782)
