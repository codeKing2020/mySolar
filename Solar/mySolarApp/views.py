from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import User
from django.db import IntegrityError

# Create your views here.
def index(request):
    return render(request, "mySolar/index.html")

def sign_in(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mySolar/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mySolar/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]

        if email == '':
            return render(request, "mySolar/register.html", {
                "message": "Enter your email address"
            })

        if username == '':
            return render(request, "mySolar/register.html", {
                "message": "Enter your username"
            })

        # Ensure unique username
        if User.objects.filter(username=username).exists():
            return render(request, "mySolar/register.html", {
                "message": "Username already exists"
            })
        
        # Ensure unique email
        if User.objects.filter(email=email).exists():
            return render(request, "mySolar/register.html", {
                "message": "Email address already exists"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mySolar/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "mySolar/register.html", {
                "message": "Error! Try use a different or longer username or email address"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mySolar/register.html")

def about(request):
    return render(request, "mySolar/about.html")

def contact(request):
    return render(request, "mySolar/contact.html")

def shop(request):
    return render(request, "mySolar/store.html")

def product(request):
    return render(request, "mySolar/product.html")

def help(request):
    return render(request, "mySolar/help.html")

def beSeller(request):
    return render(request, "mySolar/beSeller.html")

@login_required
def profileForm(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            return HttpResponse(f"Safe! You entered {form}")
        else:
            return render(request, "mySolar/test.html", {"form": form})
    else:
        form = ProfileForm()
        return render(request, "mySolar/test.html", {"form": form})