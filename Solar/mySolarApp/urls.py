from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path("profileForm", profileForm, name="profileForm"),
    path("login", sign_in, name="login"),
    path("register", register, name="register"),
    path("logout", logout_view, name="logout"),
    path("about", about, name="about"),
    path("contactUs", contact, name="contact"),
    path("shop", shop, name="shop"),
    path("product", product, name="product"),
    path("help", help, name="help"),
    path("beSeller", beSeller, name="beSeller")
]