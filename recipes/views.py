from django.shortcuts import render, redirect
from .models import User
from .models import Recipe, Ingredient, Rating
from .forms import NewRecipeForm, RatingForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count, Min, Max
from django.http import HttpResponse
from decouple import config


def home(request):
    context = {"recipes": Recipe.objects.all()}
    return render(request, "recipes/home.html", context)


def about(request):
    return render(request, "recipes/about.html")


def recipeDetail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    ingredients = recipe.ingredient_set.all().values_list("name", flat=True)
    print(recipe.ingredient_set.all().values_list("name", flat=True))

    username = request.user.username

    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            print(rating_form.cleaned_data["rating"])
            new_rating = rating_form.cleaned_data["rating"]
            rating = Rating(recipe=recipe, rating=new_rating, who_rated=username)
            rating.save()

            messages.success(
                request,
                "Recipe created successfully!",
            )
            return redirect("recipes-home")
    else:
        rating_form = RatingForm()
        voted = False
        if username in [object.who_rated for object in recipe.rating_set.all()]:
            voted = True
            print("glasao", voted)
            messages.success(
                request,
                "You have already voted on this recipe!",
            )

    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
            "rating_form": rating_form,
            "voted": voted,
            "ingredients": ingredients,
        },
    )


def userRecipes(request, username):
    user = User.objects.get(username=username)
    recipes = user.recipe_set.all()
    return render(
        request, "recipes/user_recipes.html", {"recipes": recipes, "username": username}
    )


def newRecipe(request):
    if request.method == "POST":
        ingredients = set(list(filter(None, request.POST.getlist("ingredient"))))
        ingredientNumber = len(list(filter(None, ingredients)))
        recipe = Recipe.objects.create(
            user=request.user,
            title=request.POST["title"],
            content=request.POST["content"],
            ingredientNumber=len(list(filter(None, ingredients))),
        )
        recipe.save()

        for ingredient in ingredients:
            if ingredient:
                new_ingredient = Ingredient.objects.create(
                    recipe=recipe, name=ingredient
                )
                new_ingredient.save()

        recipes = Recipe.objects.all()
        return render(request, "recipes/home.html", {"recipes": recipes})

    return render(request, "recipes/new_recipe.html")


def search(request):
    if request.method == "GET":
        search = request.GET.get("search")
        recipes = Recipe.objects.distinct().filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(ingredient__name__icontains=search)
        )
        return render(request, "recipes/search_results.html", {"recipes": recipes})


def didYouKnow(request):

    topFiveQuerySet = (
        Ingredient.objects.values("name")
        .annotate(count=Count("name"))
        .order_by("-count")[:5]
    )
    topFive = [ingr["name"] for ingr in topFiveQuerySet]

    maxIngr = Recipe.objects.all().aggregate(Max("ingredientNumber"))[
        "ingredientNumber__max"
    ]
    minIngr = Recipe.objects.all().aggregate(Min("ingredientNumber"))[
        "ingredientNumber__min"
    ]
    maxRecipe = Recipe.objects.filter(ingredientNumber=maxIngr)
    minRecipe = Recipe.objects.filter(ingredientNumber=minIngr)
    print(minRecipe)
    print(maxRecipe)

    context = {"topFive": topFive, "maxRecipe": maxRecipe, "minRecipe": minRecipe}

    return render(request, "recipes/did-you-know.html", context)