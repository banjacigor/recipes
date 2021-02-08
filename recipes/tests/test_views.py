from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from recipes.models import Recipe, Rating, Ingredient
from recipes.forms import RatingForm
from django.urls import reverse
import json

from recipes.views import (
    home,
    about,
    recipeDetail,
    userRecipes,
    newRecipe,
    search,
    didYouKnow,
)


class TestViews(TestCase):
    def setUp(self):
        self.sample_user = get_user_model().objects.create(
            username="username",
            email="johndoe@gmail.com",
            first_name="john",
            last_name="doe",
            password="password",
        )
        self.sample_recipe = Recipe.objects.create(
            user=self.sample_user,
            title="New recipe1",
            content="Instructions",
            ingredientNumber=2,
        )

        self.client = Client()
        self.home_url = reverse("recipes-home")
        self.about_url = reverse("recipes-about")
        self.recipeDetail_url = reverse("recipe-detail", kwargs={"pk": 1})
        self.userRecipes_url = reverse("user-recipes", kwargs={"username": "username"})
        self.newRecipe_url = reverse("create-new")

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/home.html")

    def test_about_GET(self):
        response = self.client.get(self.about_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/about.html")

    def test_recipeDetail_GET(self):
        response = self.client.get(self.recipeDetail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")

    def test_recipeDetail_POST(self):
        response = self.client.post(
            self.recipeDetail_url,
            {"recipe": self.sample_recipe, "rating": 2, "who_rated": "username"},
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.sample_recipe.rating_set.first().rating, 2)

    def test_userRecipes_GET(self):
        response = self.client.get(self.userRecipes_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/user_recipes.html")

    def test_newRecipe_POST(self):

        response = self.client.post(
            self.newRecipe_url,
            {
                "user": self.sample_user,
                "title": "New recipe 2",
                "content": "New content",
                "ingredientNumber": 5,
            },
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.sample_recipe.title, "New recipe 2")
