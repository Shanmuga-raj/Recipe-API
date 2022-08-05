from django.urls import reverse
from django.test import TestCase
from core.helper import create_user
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Ingredient
from ..serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        Ingredient.objects.create(name="Chicken", user=self.user)
        Ingredient.objects.create(name="Mutton", user=self.user)
        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
