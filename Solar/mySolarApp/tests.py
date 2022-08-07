from django.test import TestCase
from django.test import Client
from .models import *
from .views import *
import Solar
from django.core.exceptions import ObjectDoesNotExist

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

    def test_goodDelete(self):
        # try delete an account that does exist
        # return redirect
        # additionally ensure that user does not exist

        # login user
        c.login(username="foo", password="foo")
        # attempt to go to delete account site
        response = c.get('/delAcc')
        # assert that there is an error when trying to get user
        self.assertRaises(ObjectDoesNotExist, User.objects.get, username="foo")
        # assert that the response code is a redirect
        self.assertEqual(response.status_code, 302)

    def test_badDelete(self):
        # try to unsuccessfully delete a user that does not exist

        # first stage: login a user that does not exist
        response = c.login(username="non-existent", password="non-existent")
        self.assertFalse(response)

        # no need for other stages I believe, as long as the user is caught ebfore logging in, especially since you need to be logged in to delete your account

    def test_delete_shopkeeper_assertNoProducts(self):
        # test to see whether products of the shopkeeper remain even after deletion

        # first delete one of the products and assert that there is nothing
        product = Product.objects.get(title="solar ting")
        product.delete()

        self.assertRaises(ObjectDoesNotExist,
                          Product.objects.get, title="solar ting")

        # nothing must remain after purging the shopkeeper
        # check if profile remains after deletion
        profile = Profile.objects.get(name="bar's shop")
        profile.delete()

        self.assertRaises(ObjectDoesNotExist,
                          Profile.objects.get, name="bar's shop")

        # check if products remain after profile has been deleted
        self.assertRaises(ObjectDoesNotExist,
                          Product.objects.get, title="solar ting")
        self.assertRaises(ObjectDoesNotExist,
                          Product.objects.get, title="solar ting 2")
