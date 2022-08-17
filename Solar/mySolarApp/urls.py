from django.urls import include, path

from .views import *

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
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
    path("sellerInfo<int:seller_id>",
         sellerInfo, name="sellerInfo"),
    path("sellerProducts<int:seller_id>",
         sellerProducts, name="sellerProducts"),
    path("categoryProducts", categoryProducts, name="categoryProducts"),
    path("sellerDash", sellerDash, name="sellerDash"),
    path('createProduct', createProduct, name="createProduct"),
    path("orderInfo<int:deliveryPK><str:action>", orderInfo, name="orderInfo"),
    path("editProduct<int:productPK><str:productAction>",
         editProduct, name="editProduct"),
    path('newProduct', createProduct, name="newProduct"),
    path("userProfile", userProfile, name="userProfile"),
    path("delAcc", delAcc, name="delAcc"),
    path("areYouSure", areYouSure, name="areYouSure"),
    path("requestAction/<str:action>/<int:requestPK>",
         requestAction, name="requestAction")
]
