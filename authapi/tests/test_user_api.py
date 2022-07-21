from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "fake@email.com",
            "password": "FakePassword",
            "name": "FakeID",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_existing_user_error(self):
        payload = {
            "email": "fake@email.com",
            "password": "FakePassword",
            "name": "FakeID",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            "email": "fake@email.com",
            "password": "FP",
            "name": "FakeID",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_success(self):
        user_details = {
            "email": "fake@email.com",
            "password": "FakePassword",
            "name": "FakeID",
        }

        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_error(self):
        user_details = {
            "email": "fake@email.com",
            "password": "FakePassword",
        }

        create_user(**user_details)
        payload = {"email": "fake@email.com", "password": "WrongPassword"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {"email": "test@example.com", "password": "pass123"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password_error(self):
        user_details = {
            "email": "fake@email.com",
            "password": "",
        }
        res = self.client.post(TOKEN_URL, user_details)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
