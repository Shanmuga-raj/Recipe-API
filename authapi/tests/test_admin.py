from django.test import TestCase, Client
from django.urls import reverse
from core.helper import create_user, create_superuser


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = create_superuser()
        self.client.force_login(self.admin_user)
        self.user = create_user()

    def test_users_list(self):
        url = reverse("admin:authapi_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        url = reverse("admin:authapi_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse("admin:authapi_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
