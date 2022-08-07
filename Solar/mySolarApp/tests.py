from urllib import response
from django.test import TestCase
from django.test import Client
from .models import *
from .views import *
import Solar
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth

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
        self.buyerDict = {
            "username": "foo",
            "email": "foo@gmail.com",
            "password": "foo"
        }
        # create seller
        seller = User.objects.create_user(
            "bar", "bar@gmail.com", "bar", is_shopkeeper=True)
        self.sellerDict = {
            "username": "bar",
            "email": "bar@gmail.com",
            "password": "bar"
        }
        # create profile linked to seller
        profile = Profile.objects.create(
            shopkeeper=seller, name="bar's shop", bio="my shop",
            location="bar street", how_active=2, identification="1234567890qwe"
        )
        self.profileDict = {
            "shopkeeper": seller,
            "name": "bar's shop",
            "bio": "my shop",
            "location": "bar_street",
            "how_active": 2,
            "identification": "1234567890qwe"
        }
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
        self.product1Dict = {
            "seller": profile,
            "title": "solar ting",
            "short_desc": "short",
            "long_desc": "long story short",
            "category": "MISC",
            "price": 23,
            "in_stock": True
        }
        Product2 = Product.objects.create(
            seller=profile,
            title="solar ting 2",
            short_desc="shorty",
            long_desc="longy story shorty",
            category="ACC",
            price=24,
            in_stock=True
        )
        self.product2Dict = {
            "seller": profile,
            "title": "solar ting 2",
            "short_desc": "shorty",
            "long_desc": "longy story shorty",
            "category": "ACC",
            "price": 24,
            "in_stock": True
        }
    # now to test our data

    def test_registerUser(self):
        """
        alter dictionary declared to fit the name of our smaple user
        check if our user (not yet created) is present
        register the user
        check if the user now exists
        check if the user is a user, not a shopkeeper or superuser
        check if we got redirected back to index, meaning user got registered correctly
        """
        # register our user
        # make a sample user to work with using dictionaries declared at top
        self.buyerDict["username"] = "gorilla"
        user = User.objects.filter(username=self.buyerDict["username"])
        # check if user was present before
        # check by asserting that the number of users with username Gorilla is 0
        self.assertEqual(len(user), 0)
        # post a request to register the user
        response = c.post(
            '/register', {"username": "gorilla", "email": "gorilla@gmail.com", "password": "foo", "confirmation": "foo"})
        # make sure user is now present
        # make second call to model
        user = User.objects.filter(username=self.buyerDict["username"])
        # count number of users with name gorilla present
        self.assertEqual(len(user), 1)
        # make sure user is a user, not shopkeeper or staff or superuser
        user = user.first()
        self.assertFalse(user.is_shopkeeper)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # make sure that we get a redirect, meaning they got registered, and are being redirected to index
        self.assertEqual(response.status_code, 302)

    def test_registerUserWrongUsername(self):
        # register our user but wrong username
        response = c.post(
            '/register', {"username": "foo", "email": "foo@gmail.com", "password": "foo", "confirmation": "foo"})
        self.assertContains(response, "Username already exists")

    def test_registerUserWrongEmail(self):
        # register our user but wrong email
        response = c.post(
            '/register', {"username": "dietz", "email": "foo@gmail.com", "password": "foo", "confirmation": "foo"})
        self.assertContains(response, "Email address already exists")

    def test_registerUserWrongPassword(self):
        # register our user but wrong password
        response = c.post(
            '/register', {"username": "gully", "email": "gully@gmail.com", "password": "foozy", "confirmation": "foo"})
        self.assertContains(response, "Passwords must match.")

    def test_signIn(self):
        # sign in our user successfully
        # verify whether the user has been logged in
        # by checking if there is a user that is authenticated
        # in the auth module
        """
        Original text:
        You can use the get_user method of the auth module. It says it wants a request as parameter, but it only ever uses the session attribute of the request. And it just so happens that our Client has that attribute.
        https://stackoverflow.com/questions/5660952/test-that-user-was-logged-in-successfully/35871564#35871564
        """
        response = c.post('/login', {"username": "foo", "password": "foo"})

        user = auth.get_user(c)
        self.assertTrue(user.is_authenticated)

        self.assertEqual(response.status_code, 302)

    def test_signInWrongPassword(self):
        # sign in our user incorrectly
        # correct username but wrong password
        response = c.post('/login', {"username": "foo", "password": "foozy2"})
        self.assertContains(response, "Invalid username and/or password.")

    def test_signInWrongUsername(self):
        # incorrect username but correct password
        response = c.post('/login', {"username": "barry", "password": "bar"})
        self.assertContains(response, "Invalid username and/or password.")

    def test_goodDelete(self):
        # try delete an account that does exist
        # return redirect
        # additionally ensure that user does not exist
        user = User.objects.filter(username=self.buyerDict["username"])
        # test user exists
        self.assertEqual(len(user), 1)
        # login user
        c.login(username=self.buyerDict["username"],
                password=self.buyerDict["password"])
        # attempt to go to delete account site
        response = c.get('/delAcc')
        # assert that there is an error when trying to get user
        self.assertRaises(ObjectDoesNotExist, User.objects.get,
                          username=self.buyerDict["username"])
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

    """
    NOW FOR THE OTHER PAGES
    """

    def test_about_view(self):
        # test to see if we get about page
        # get the page and check status code returned
        response = c.get("/about")
        self.assertEqual(response.status_code, 200)

        # assert there is a certain text in the content
        self.assertContains(response, "About")

    def test_contact_view(self):
        # test to see if we get contact page
        # get the page and check status code returned
        response = c.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        # get page
        response = c.get(reverse("contact"))
        # assert there is a certain text in the content
        self.assertContains(response, "Connect with Us")

    def test_shop_pageAllProducts(self):
        # get page
        # test to see if products are listed
        # check if products exist in model
        self.assertEqual(len(Product.objects.filter(
            title=self.product1Dict['title'])), 1)
        self.assertEqual(len(Product.objects.filter(
            title=self.product2Dict['title'])), 1)

        response = c.get("/shop")
        self.assertContains(response, self.product1Dict['title'])
        self.assertContains(response, self.product2Dict['title'])

    def test_shop_pageOneProduct(self):
        # remove a product
        # again test to see if product is not displaying and also shows others
        self.assertEqual(len(Product.objects.filter(
            title=self.product1Dict['title'])), 1)
        Product.objects.filter(title=self.product2Dict['title']).delete()
        self.assertEqual(len(Product.objects.filter(
            title=self.product2Dict['title'])), 0)

        # get shop page
        response = c.get("/shop")
        # assert that shop contains one product
        self.assertContains(response, self.product1Dict['title'])
        # assert that the deleted product does not contain the product
        self.assertNotContains(response, self.product2Dict['title'])

    def test_no_products(self):
        # finally delete all products
        Product.objects.all().delete()
        self.assertEqual(len(Product.objects.all()), 0)
        # get to shop page
        response = c.get("/shop")
        # assert that shop has nothing
        # check that store.html has no results
        self.assertContains(
            response, "There are no products in this category yet")

    def test_product_info(self):
        product = Product.objects.get(title=self.product1Dict['title'])
        """
        request page
        expect response
        expect certain product
        """
        response = c.get(f"/product{product.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1Dict['title'])

    def test_nonExistent_productInfo(self):
        """
        delete product
        request page again
        expect message
        """
        product = Product.objects.get(title=self.product1Dict['title'])
        productPK = product.pk
        product.delete()
        self.assertRaises(ObjectDoesNotExist, Product.objects.get,
                          title=self.product1Dict['title'])

        response = c.get(f"/product{productPK}")
        self.assertEqual(response.status_code, 404)

    def test_seller_info(self):
        seller = Profile.objects.get(name=self.profileDict['name'])
        """
        request page
        expect response
        expect certain seller
        """
        response = c.get(f"/sellerInfo{seller.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profileDict['bio'])

    def test_nonExistent_sellerInfo(self):
        """
        delete seller
        request page again
        expect message
        """
        seller = Profile.objects.get(name=self.profileDict['name'])
        sellerPK = seller.pk
        seller.delete()
        self.assertRaises(ObjectDoesNotExist, Profile.objects.get,
                          name=self.profileDict['name'])

        response = c.get(f"/product{sellerPK}")
        self.assertEqual(response.status_code, 404)

    def test_beSellerRequest(self):
        """
        user request
        expect certain response and message
        """
        # user has to be logged in first
        # so login buyer first because they have the "authority"
        c.login(username=self.buyerDict["username"],
                password=self.buyerDict["password"])
        # fill in form and send
        response = c.post("beSeller", )

    def test_beSellerReRequest(self):
        """
        user re-request
        expect certain message
        """
        pass

    def test_beSellerAlreadyShopkeeper(self):
        """
        user who is already shopkeeper
        expect response and message
        """
        pass

    def test_beSellerAlreadySubmitted(self):
        # for the wanna be buyers that want to request again to be a seller
        pass

    def testRequestsAndQuestions(self):
        # test by checking requests

        # test by checking questions
        # check how many questions there are when request
        # delete the question
        # check again
        pass
