from django import forms
from django.forms import ModelForm
from .models import Recipe


class NewRecipeForm(forms.ModelForm):
    class Meta:

        model = Recipe
        fields = ["title", "content"]


RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]


class RatingForm(forms.Form):
    rating = forms.IntegerField(
        label="Rate this recipe.", widget=forms.RadioSelect(choices=RATING_CHOICES)
    )
