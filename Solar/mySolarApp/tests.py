from django.test import TestCase
from django.test import Client
from .models import *
from .views import *
import Solar

Solar.settings.ALLOWED_HOSTS += ['127.0.0.1', 'localhost', 'testserver', ]
c = Client()


class UserTestCase(TestCase):

    def setUp(self):
        """
        Create our sample data:
            user field, one buyer, the other a seller
            create profile and products linked to seller
        """

        # create buyer
        buyer = User.objects.create_user("foo", "foo@gmail.com", "foo")

        # create seller
        seller = User.objects.create_user(
            "bar", "bar@gmail.com", "bar", is_shopkeeper=True)

        # create profile linked to seller
        profile = Profile.objects.create(
            shopkeeper=seller, name="bar's shop", bio="my shop",
            location="bar street", how_active=2, identification="1234567890qwe"
        )

        # create 2 products linked to seller
        Product1 = Product.objects.create(
            seller=profile,
            title="solar ting",
            short_desc="short",
            long_desc="long story short",
            category="MISC",
            price=23,
            in_stock=True
        )

        Product2 = Product.objects.create(
            seller=profile,
            title="solar ting 2",
            short_desc="shorty",
            long_desc="longy story shorty",
            category="ACC",
            price=24,
            in_stock=True
        )

    # now to test our data
    def test_registerUser(self):
        # register our user
        response = c.post(
            '/register', {"username": "gorilla", "email": "gorilla@gmail.com", "password": "foo", "confirmation": "foo"})
        # make sure that we get a redirect, meaning they got registered, and are being redirected to index
        self.assertEqual(response.status_code, 302)

    def test_registerUserGoneWrong(self):
        # register our user but it doesn't work
        response = c.post(
            '/register', {"username": "foo", "email": "foo@gmail.com", "password": "foo", "confirmation": "foo"})
        self.assertContains(response, "Username already exists")

        response = c.post(
            '/register', {"username": "dietz", "email": "foo@gmail.com", "password": "foo", "confirmation": "foo"})
        self.assertContains(response, "Email address already exists")

        response = c.post(
            '/register', {"username": "gully", "email": "gully@gmail.com", "password": "foozy", "confirmation": "foo"})
        self.assertContains(response, "Passwords must match.")

    def test_signIn(self):
        # sign in our user successfully
        response = c.post('/login', {"username": "foo", "password": "foo"})
        self.assertEqual(response.status_code, 302)

    def test_signInGoneWrong(self):
        # sign in our user incorrectly
        # correct username but wrong password
        response = c.post('/login', {"username": "foo", "password": "foozy2"})
        self.assertContains(response, "Invalid username and/or password.")

        # incorrect username but correct password
        response = c.post('/login', {"username": "barry", "password": "bar"})
        self.assertContains(response, "Invalid username and/or password.")
