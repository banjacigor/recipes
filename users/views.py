from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler


from .serializers import UserSerializer
from django.conf import settings
from .models import User
import jwt

from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employment
import requests
import clearbit
from decouple import config


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get("user", {})

        serializer = UserSerializer(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def authenticate_user(request):

    try:
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details["name"] = "%s %s" % (user.first_name, user.last_name)
                user_details["token"] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                "error": "can not authenticate with the given credentials or the account has been deactivated"
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {"error": "please provide a email and a password"}
        return Response(res)


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        HUNTER_SECRET_KEY = config("HUNTER_SECRET_KEY")

        url = "https://api.hunter.io/v2/email-verifier?email={}&api_key={}"

        if user_form.is_valid():

            email = user_form.cleaned_data.get("email")
            r = requests.get(url.format(email, HUNTER_SECRET_KEY)).json()
            status = r["data"]["status"]

            if status not in ["invalid", "unknown"]:

                username = user_form.cleaned_data.get("username")
                user_form.save()

                messages.success(
                    request,
                    f"Account created for { email }! You are now able to log in!",
                )
                return redirect("login")
            else:
                messages.error(request, "Please enter valid email address.")
                return redirect("register")

    else:
        user_form = UserRegisterForm()

    return render(
        request,
        "users/register.html",
        {"user_form": user_form},
    )


@login_required
def profile(request):
    return render(request, "users/profile.html")