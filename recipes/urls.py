from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="recipes-home"),
    path("about/", views.about, name="recipes-about"),
    path("recipe/<int:pk>/", views.recipeDetail, name="recipe-detail"),
    path("user/<str:username>/", views.userRecipes, name="user-recipes"),
    path("create/", views.newRecipe, name="create-new"),
    path("search/", views.search, name="search"),
    path("did_you_know/", views.didYouKnow, name="did-you-know"),
]