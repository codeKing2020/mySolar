from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path("profileForm", profileForm, name="profileForm"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("logout", logout_view, name="logout"),
]