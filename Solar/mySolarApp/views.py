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

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mySolar/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "mySolar/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mySolar/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "mySolar/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mySolar/register.html")

def test(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            return HttpResponse(f"Safe! You entered {form}")
        else:
            return HttpResponse(f"Not Safe! You entered {form}")
    else:
        form = UserForm()
        return render(request, "mySolar/test.html", {"form": form})



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