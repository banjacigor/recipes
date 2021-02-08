from django.test import TestCase
from django.urls import reverse, resolve
from recipes.views import (
    home,
    about,
    recipeDetail,
    userRecipes,
    newRecipe,
    search,
    didYouKnow,
)


class TestUrls(TestCase):
    def test_recipes_home_url(self):
        url = reverse("recipes-home")
        self.assertEquals(resolve(url).func, home)

    def test_about_url(self):
        url = reverse("recipes-about")
        self.assertEquals(resolve(url).func, about)

    def test_recipe_detail_url(self):
        url = reverse("recipe-detail", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func, recipeDetail)

    def test_user_recipes_url(self):
        url = reverse("user-recipes", kwargs={"username": "JohnDoe"})
        self.assertEquals(resolve(url).func, userRecipes)

    def test_create_url(self):
        url = reverse("create-new")
        self.assertEquals(resolve(url).func, newRecipe)

    def test_search_url(self):
        url = reverse("search")
        self.assertEquals(resolve(url).func, search)

    def test_did_you_know_url(self):
        url = reverse("did-you-know")
        self.assertEquals(resolve(url).func, didYouKnow)