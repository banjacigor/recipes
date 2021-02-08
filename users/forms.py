from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:

        model = User

        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]