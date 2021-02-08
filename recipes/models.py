from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Max, Min, Sum


class Recipe(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    ingredientNumber = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or ""

    def snippet(self):
        return self.content[:20] + "..."

    @property
    def average_rating(self):

        all_ratings = self.rating_set.all()
        n = self.rating_set.all().count()
        total = sum([one_rating.rating for one_rating in all_ratings])
        if n == 0:
            return 0
        else:
            return round(total / n, 1)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    who_rated = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.rating)
