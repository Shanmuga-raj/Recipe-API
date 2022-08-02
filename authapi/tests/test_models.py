from django.test import TestCase
from core.helper import create_user, create_superuser


class ModelTests(TestCase):
    def test_create_user_with_email_success(self):
        user = create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.com", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = create_user(email, "TestPassword")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            create_user("", "TestPassword")

    def test_create_superuser(self):
        user = create_superuser()

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
