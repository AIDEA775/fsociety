from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model


def index(request):
    if request.user.is_authenticated:
        return redirect('video_room:feed')
    else:
        return render(request, "login/index.html")


@csrf_protect
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('video_room:feed')
    else:
        context = {'error_message': 'Wrong username or password'}
        return render(request, "login/index.html", context)


@csrf_protect
def signup(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    try:
        validate_email(email)
    except ValidationError:
        context = {'error_message': 'The email address is not valid'}
        return render(request, "login/index.html", context)

    if all([first_name, last_name, email, password]):
        try:
            get_user_model().objects.create_user(email, email, password,
                                                 first_name=first_name,
                                                 last_name=last_name)
            user = authenticate(username=email, password=password)
            auth_login(request, user)
            return redirect('video_room:feed')
        except IntegrityError:
            context = {'error_message': 'Email is already in use'}
            return render(request, "login/index.html", context)
    else:
        context = {'error_message': 'A field is empty'}
        return render(request, "login/index.html", context)
