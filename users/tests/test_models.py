from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_successful(self):
        email = "test@gmail.com"
        username = "testuser"
        password = "test123456789"
        first_name = "test"
        last_name = "user"
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))