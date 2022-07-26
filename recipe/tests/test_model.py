from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Recipe


class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            "fake@email.com",
            "FakePassword",
        )
        recipe = Recipe.objects.create(
            user=user,
            title="Simple Recipe",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Simple Recipe Description",
        )

        self.assertEqual(str(recipe), recipe.title)
