from django.urls import reverse
from django.test import TestCase
from core.helper import create_user
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Tag
from ..serializers import TagSerializer

TAG_URL = reverse("recipe:tag-list")


class PublicTagApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tag(self):
        Tag.objects.create(name="Vegan", user=self.user)
        Tag.objects.create(name="Dessert", user=self.user)
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = create_user(email="FakeUser2@email.com")
        Tag.objects.create(name="Fruits", user=user2)
        tag = Tag.objects.create(name="Junk Food", user=self.user)

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)
