from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path("test", test, name="test"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("logout", logout_view, name="logout"),
]