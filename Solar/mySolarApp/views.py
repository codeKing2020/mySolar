import re
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
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
        return render(request, "mySolar/index.html")
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
    f = Product.objects.all()
    categoryForm = categoryProductsForm()
    if len(f) != 0:
        context = {
            "products": f,
            "categoryForm": categoryForm
        }
    else:
        context = {"products": "None"}
    return render(request, "mySolar/store.html", context)


def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        "product": product
    }
    return render(request, "mySolar/product.html", context)


def sellerInfo(request, seller_id):
    seller = Profile.objects.get(pk=seller_id)
    context = {
        "seller": seller,
    }
    return render(request, "mySolar/seller.html", context)


def sellerProducts(request, seller_id):
    try:
        # try to access seller through seller id
        seller = Profile.objects.get(pk=seller_id)
        sellerProducts = Product.objects.filter(seller=seller)
    except Exception:
        # else it must be a user id
        user = User.objects.get(pk=seller_id)
        seller = user.user_profile
        sellerProducts = Product.objects.filter(
            seller=seller.pk)
    context = {
        "products": sellerProducts
    }
    return render(request, "mySolar/store.html", context)


def success(request):
    return render(request, "mySolar/success.html")


@login_required
def beSeller(request):
    # Get User
    USER = request.user
    # Get user in database by their username
    a = User.objects.get(username=USER.get_username())
    # if the user already submitted the form before
    if a.beSellerFormSubmitted:
        # create context dict
        context = {
            "success": "alreadyApplied",
        }
        # redirect to success page
        return render(request, "mySolar/success.html", context)

    # else user hasn't submitted before
    # if user submitted
    elif request.method == 'POST':
        # process form
        user_form = SellerRequestForm(request.POST)
        # if form is valid
        if user_form.is_valid():
            # add user info in the instance
            user_form.instance.sellerAcc = USER
            # save the info
            user_form.save()
            # set user submitForm to true
            a.beSellerFormSubmitted = True
            a.save()
            # redirect to success page
            return render(request, 'mySolar/success.html', {"success": "pendingSellerConfirmation"})

        # else form isn't valid
        else:
            # create context dict which stores errors and other stuff
            context = {
                'user_form': user_form,
            }
    # else user hasn't submitted form before and also isn't right now
    else:
        # create context with the form
        context = {
            'user_form': SellerRequestForm(),
        }

    # go to original page
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


@login_required
def requestsAndQuestions(request):
    if request.user.is_staff == False or request.user.is_superuser == False:
        return render(request, "mySolar/fail.html", {'message': "You are not permitted here."})
    else:
        requests = sellerRequests.objects.all()
        QUESTIONS = userQuestions.objects.all()
        return render(request, "mySolar/requestsAndQuestions.html", {"requests": requests, "questions": QUESTIONS})


def categoryProducts(request):
    if request.method == 'POST':
        # process form
        user_form = categoryProductsForm(request.POST)
        # if form is valid
        if user_form.is_valid():
            # get products in that category
            user_data = user_form.cleaned_data.get("category")
            products = Product.objects.filter(category=user_data)
            user_form = categoryProductsForm(request.POST)
            if len(products) < 1:
                products = "None"
            context = {
                "categoryForm": user_form,
                "products": products
            }
            # redirect with those products
            return render(request, 'mySolar/store.html', context)

        # else form isn't valid
        else:
            # create context dict which stores errors and other stuff
            context = {
                'user_form': user_form,
            }

            return render(request, 'mySolar/store.html', context)


@login_required
def sellerDash(request):
    if request.user.is_shopkeeper:
        # return info about the user/shopkeeper
        # return info about deliveries concerning the user themselves
        user = request.user.id
        profile = Profile.objects.get(shopkeeper=user)
        delivery_items = delivery_info.objects.filter(seller=profile)
        if len(delivery_items) != 0:
            context = {
                "user": User.objects.get(username=request.user.username),
                "delivery_info": delivery_items
            }
        else:
            context = {
                "user": User.objects.get(username=request.user.username),
                "delivery_info": "empty"
            }
        return render(request, "mySolar/sellerDash.html", context)
    return render(request, "mySolar/fail.html", {"message": "You are not authorized to enter this page."})


@login_required
def createProduct(request):
    if request.user.is_shopkeeper or request.user.is_staff:
        if request.method == "POST":
            product_form = createProductForm(request.POST)
            # if form is valid
            if product_form.is_valid():
                # access user through user model
                user = User.objects.get(pk=request.user.pk)
                seller = user.user_profile
                # punch in seller to product form instance
                product_form.instance.seller = seller
                # take info and save
                product_form.save()
                # redirect to product page
                return product(request, product_form.instance.pk)
        else:
            product_form = createProductForm()
            return render(request, "mySolar/newProduct.html", {"product_form": product_form})
    else:
        return render(request, "mySolar/fail.html", {"message": "You are not authorized to be on this page."})


def orderInfo(request, deliveryPK, action):
    if action == "view":
        # search up delivery info
        # send to page with info
        info = delivery_info.objects.get(pk=deliveryPK)
        return render(request, "mySolar/orderInfo.html", {"info": info})
    elif action == "process":
        # search up delivery info
        # alt info
        # send to page with info
        info = delivery_info.objects.get(pk=deliveryPK)
        info.processed = True
        info.save()
        return render(request, "mySolar/orderInfo.html", {"info": info})
    elif action == "delivered":
        # search up delivery info
        # alt info
        # send to page with info
        orderInfo(request, deliveryPK, "process")
        info = delivery_info.objects.get(pk=deliveryPK)
        info.delivered = True
        info.save()
        return render(request, "mySolar/orderInfo.html", {"info": info})
    elif action == "delete":
        # search up delivery info
        # send to page with info
        info = delivery_info.objects.get(pk=deliveryPK)
        info.delete()
        return sellerDash(request)
    else:
        return render(request, "mySolar/fail.html", {'message': "We don't know why you're here. <br> Seeing this page by mistake? Contact us! Go to the help page and submit a query."})


def editProduct(request, productPK, productAction):
    # take product
    # if it's for editing
    # return form page
    # take in info given and do something with it (has to be inside the same if statement but also in an is post method statement)
    # redirect to finished product (just return function of viewProduct ting)
    # else if it's for deleting
    # take the post
    # delete it
    # redirect to products page
    productObject = Product.objects.get(pk=productPK)
    if productAction == "edit":
        if request.method == "GET":
            productForm = createProductForm(instance=productObject)
            return render(request, 'mySolar/createProduct.html', {"form": productForm, "productPK": productPK})
        elif request.method == "POST":
            # process form
            product_form = createProductForm(request.POST)
            # if form is valid
            if product_form.is_valid():
                # add user info
                product_form.instance.seller = productObject.seller
                # save
                product_form.save()
                # delete productObject to make way for the other one
                Product.objects.get(pk=productPK).delete()
                # redirect to product page
                return product(request, product_form.instance.pk)
            else:
                # create context dict which stores errors and other stuff
                return render(request, 'mySolar/createProduct.html', {"form": product_form, "productPK": productPK})
    elif productAction == "delete":
        productObject.delete()
        return sellerProducts(request, productObject.seller.pk)


@login_required
def sellerProfile(request):
    # if get request
    # create form out of user instance
    # create form out of profile instance
    # serve out
    # else if post request
    # process it
    # update/save
    # recurse (call function again but this time being a get request)
    if request.method == "GET":
        if request.user.is_shopkeeper:
            shopkeeperObject = Profile.objects.get(
                shopkeeper=request.user)
            shopkeeperForm = sellerProfileForm(instance=shopkeeperObject)
            userObject = User.objects.get(pk=request.user.pk)
            userForm = userProfileForm(instance=userObject)
            context = {
                "userForm": userForm,
                "shopkeeperForm": shopkeeperForm
            }
            return render(request, "mySolar/userProfile.html", context)
        elif request.user.is_shopkeeper == False:
            userObject = User.objects.get(pk=request.user.pk)
            userForm = userProfileForm(instance=userObject)
            context = {
                "userForm": userForm,
            }
            return render(request, "mySolar/userProfile.html", context)
        else:
            return render(request, "mySolar/fail.html", {"message": "You are not authorized to be on this page."})
    else:
        if request.user.is_shopkeeper:
            user_profile_form = userProfileForm(request.POST)
            shopkeeper_profile_form = sellerProfileForm(request.POST)
            if user_profile_form.is_valid() and shopkeeper_profile_form.is_valid():
                # don't forget to add user info!
                return HttpResponse(f"valid! {user_profile_form} and {shopkeeper_profile_form}")
            else:
                return render(request, "mySolar/userProfile.html", {"userForm": user_profile_form, "shopkeeperForm": shopkeeper_profile_form})
        elif request.user.is_shopkeeper == False:
            user_profile_form = userProfileForm(request.POST)
            if user_profile_form.is_valid():
                # don't forget to add user info!
                return HttpResponse(f"valid! {user_profile_form}")
            else:
                return render(request, "mySolar/userProfile.html", {"userForm": user_profile_form})


@login_required
def delAcc(request):
    # take user from request
    # take object from model
    # delete
    # redirect
    user = User.objects.get(pk=request.user.pk)
    user.delete()
    return redirect("/")


@login_required
def areYouSure(request):
    return render(request, "mySolar/areYouSure.html")
