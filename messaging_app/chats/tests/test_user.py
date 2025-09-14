from django.test import TestCase
from chats.models import User

class UserCreationTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='user1@example.com',
            password='password123',
            first_name='User ',
            last_name='One',
            role='guest'
        )
        self.assertEqual(user.email, 'user1@example.com')
        self.assertTrue(user.check_password('password123'))  # verifies password hashing
        self.assertEqual(user.first_name, 'User ')
        self.assertEqual(user.last_name, 'One')
        self.assertEqual(user.role, 'guest')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            first_name='Admin',
            last_name='User ',
            role='admin'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpass'))
        self.assertEqual(admin_user.role, 'admin')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='password123'
            )
