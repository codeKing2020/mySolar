from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import User
from django.db import IntegrityError
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, "mySolar/index.html")

def sign_in(request):
    # get the next info from the POST area (forms)
    next_page = request.POST.get('next')
    # if the user is authenticated
    if request.user.is_authenticated:
        if next_page is not None:
            return HttpResponseRedirect(next_page)
        return HttpResponseRedirect("index")
    else:
        if request.method == "POST":
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                # keep user info in session
                login(request, user)
                # if there is a page they have to go to next
                if next_page is not None:
                    # go to it
                    return HttpResponseRedirect(next_page)
                # else just redirect to the home page
                return HttpResponseRedirect(reverse("index"))
            # there were wrong details entered
            else:
                return render(request, "mySolar/login.html", {
                    "message": "Invalid username and/or password."
                })
        # this was a GET request    
        else:
            return render(request, "mySolar/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    # if we received a POST method request
    if request.method == "POST":
        # take email and username info
        email = request.POST["email"]
        username = request.POST["username"]

        # ensure email field isn't empty
        if email == '':
            return render(request, "mySolar/register.html", {
                "message": "Enter your email address"
            })

        # ensure username field isn't empty
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
    # else our request method is a GET request
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

@login_required
def success(request):
    return render(request, "mySolar/success.html")

@login_required
def beSeller(request):
    if request.method == 'POST':
        
        user_form = SellerRequestForm(request.POST)

        if user_form.is_valid():
            user_form.instance.sellerAcc = request.user
            user_form.save()
            return redirect('/success', success="pendingSellerConfirmation")        

        else:
            context = {
                'user_form': user_form,
            }

    else:
        context = {
            'user_form': SellerRequestForm(user=request.user),
        }

    return render(request, "mySolar/beSeller.html", context)

def help(request):
    if request.method == "POST":
        question_form = askQuestionForm(request.POST)

        if question_form.is_valid():
            question_form.save()
            return redirect('/success', success="pendingHelp")
        else:
            context = {
                'question_form': question_form,
            }
    else:
        context = {
            'question_form': askQuestionForm(),
        }

    return render(request, "mySolar/help.html", context)
