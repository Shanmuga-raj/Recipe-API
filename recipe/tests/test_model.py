from decimal import Decimal
from django.test import TestCase
from ..models import Recipe, Tag
from core.helper import create_user


class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        user = create_user()
        recipe = Recipe.objects.create(
            user=user,
            title="Simple Recipe",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Simple Recipe Description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = Tag.objects.create(name="Tag 1", user=user)

        self.assertEqual(str(tag), tag.name)