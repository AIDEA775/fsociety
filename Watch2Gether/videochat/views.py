from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from videochat.models import CustomUser

def index(request):
    """Index view, displays login mechanism"""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "videochat/index.html")


@login_required
def home(request):
    return render(request, 'videochat/home.html')

def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('home')
    else:
        return redirect('index')

def signup(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if all([first_name, last_name, email, password]):
        user = CustomUser.objects.create_user(first_name=first_name,
                          last_name=last_name,
                          email=email,
                          username=email)
        user.set_password(password)
        user.save()
        return redirect('home')
    else:
        return redirect('index')
