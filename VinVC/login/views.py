from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from login.models import CustomUser

def index(request):
    """Index view, displays login mechanism"""
    if request.user.is_authenticated:
        return redirect('user:index')
    else:
        return render(request, "login/index.html")


def login(request):
    """Loginn user from POST data"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('user:index')
    else:
        return redirect('login:index')


def signup(request):
    """Register a new user from POST data"""
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if all([first_name, last_name, email, password]):
        try:
            CustomUser.objects.create_user(email, email, password,
                                           first_name=first_name,
                                           last_name=last_name)
            # All okay
            user = authenticate(username=email, password=password)
            auth_login(request, user)
            return redirect('user:index')
        except IntegrityError:
            # Email is already in use
            return redirect('login:index')
    else:
        # A field is empty
        return redirect('login:index')
