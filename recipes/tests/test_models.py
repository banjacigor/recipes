from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Ingredient, Rating


class ModelTest(TestCase):
    def setUp(self):
        email = "test@gmail.com"
        username = "testuser"
        password = "test123456789"
        first_name = "test"
        last_name = "user"
        self.sample_user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.sample_recipe = Recipe.objects.create(
            user=self.sample_user,
            title="New recipe",
            content="New content",
            ingredientNumber=5,
        )

    def test_create_recipe_successfull(self):

        self.assertEqual(self.sample_recipe.title, "New recipe")
        self.assertEqual(self.sample_recipe.content, "New content")
        self.assertEqual(self.sample_recipe.ingredientNumber, 5)

    def test_create_ingredient_successfull(self):

        self.sample_ingredient = Ingredient.objects.create(
            recipe=self.sample_recipe, name="zucchini"
        )

        self.assertEqual(self.sample_ingredient.name, "zucchini")

    def test_create_rating_successfull(self):

        self.sample_rating = Rating.objects.create(
            recipe=self.sample_recipe, rating=5, who_rated="unknown user"
        )

        self.assertEqual(self.sample_rating.rating, 5)
        self.assertEqual(self.sample_rating.who_rated, "unknown user")
