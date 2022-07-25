from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path("login", sign_in, name="login"),
    path("register", register, name="register"),
    path("logout", logout_view, name="logout"),
    path("about", about, name="about"),
    path("contactUs", contact, name="contact"),
    path("shop", shop, name="shop"),
    path("product<int:product_id>", product, name="product"),
    path("help", help, name="help"),
    path("beSeller", beSeller, name="beSeller"),
    path("success", success, name="success"),
    path("requestsAndQuestions", requestsAndQuestions, name="requests"),
    path("sellerInfo<int:seller_id>", sellerInfo, name="sellerInfo"),
    path("sellerProducts<int:seller_id>",
         sellerProducts, name="sellerProducts"),
    path("categoryProducts", categoryProducts, name="categoryProducts"),
    path("sellerDash", sellerDash, name="sellerDash"),
    path('createProduct', createProduct, name="createProduct"),
    path("orderInfo<int:deliveryPK>", orderInfo, name="orderInfo")
]
