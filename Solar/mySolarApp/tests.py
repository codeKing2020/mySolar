from datetime import datetime, timezone
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
        # create question
        userQuestions.objects.create(
            email="foo@test.com",
            question="Can I get a hunyah!?"
        )
        # create superuser/staff
        User.objects.create_user(
            "king", "king@king.com", "king", is_staff=True, is_superuser=True)

        order = delivery_info.objects.create(
            seller=profile,
            item=Product1,
            amount_of_item=1,
            customer=buyer,
            delivery_date=datetime.now(tz=timezone.utc),
            location="123 foo street"
        )

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

        # no need for other stages I believe, as long as the user is caught before logging in, especially since you need to be logged in to delete your account

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
        # assert that user hasn't submitted form yet
        self.assertFalse(User.objects.get(
            username=self.buyerDict['username']).beSellerFormSubmitted)
        # fill in form and send
        response = c.post("/beSeller", {
            "name": "Goofy Industries",
            "sellerFName": 'goof',
            "sellerLName": 'ball',
            "businessEmail": 'goofball@gmail.com',
            "businessContact": int("02927323122"),
            "identification": int("02927323122"),
            "bio": "keeping it goofy",
            "location": "Goofy street"
        })
        # it must pass
        # if it has passed:
        # we must see beSellerFormSubmitted set to True
        # and we must see that there is a new entry, find it by using User model
        # we are rendered a page (200 OK)
        user = User.objects.get(username=self.buyerDict['username'])
        self.assertEqual(len(sellerRequests.objects.filter(sellerAcc=user)), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.beSellerFormSubmitted)

    def test_beSellerRequest_AGAIN(self):
        # for the wanna be buyers that want to request again to be a seller
        """
        user request
        user re-request
        expect certain message
        """
        # user has to be logged in first
        # so login buyer first because they have the "authority"
        c.login(username=self.buyerDict["username"],
                password=self.buyerDict["password"])
        # assert that user hasn't submitted form yet
        self.assertFalse(User.objects.get(
            username=self.buyerDict['username']).beSellerFormSubmitted)
        # fill in form and send
        response = c.post("/beSeller", {
            "name": "Goofy Industries",
            "sellerFName": 'goof',
            "sellerLName": 'ball',
            "businessEmail": 'goofball@gmail.com',
            "businessContact": int("02927323122"),
            "identification": int("02927323122"),
            "bio": "keeping it goofy",
            "location": "Goofy street"
        })
        # it must pass
        # if it has passed:
        # we must see beSellerFormSubmitted set to True
        # and we must see that there is a new entry, find it by using User model
        # we are rendered a page (200 OK)
        user = User.objects.get(username=self.buyerDict['username'])
        self.assertEqual(len(sellerRequests.objects.filter(sellerAcc=user)), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.beSellerFormSubmitted)

        # re-request
        response = c.post("/beSeller", {
            "name": "Goofy Industries",
            "sellerFName": 'goof',
            "sellerLName": 'ball',
            "businessEmail": 'goofball@gmail.com',
            "businessContact": int("02927323122"),
            "identification": int("02927323122"),
            "bio": "keeping it goofy",
            "location": "Goofy street"
        })

        # assert that we are rendered a new page
        self.assertEqual(response.status_code, 200)
        # assert that we are told that we are not allowed to re-apply
        self.assertContains(
            response, "You have already applied to become a seller")
        # assert that no new records were made
        # first search for sellerRequest field that matches our user
        sellerRequest = sellerRequests.objects.filter(sellerAcc=user)
        self.assertEqual(len(sellerRequest), 1)

        # assert that beSellerFormSubmitted is True
        self.assertTrue(user.beSellerFormSubmitted)

    def test_beSellerAlreadyShopkeeper(self):
        """
        user who is already shopkeeper tries to request
        expect response and message
        """
        # user has to be logged in first
        # so login seller first
        c.login(username=self.sellerDict["username"],
                password=self.sellerDict["password"])
        # assert that user hasn't submitted form yet
        self.assertFalse(User.objects.get(
            username=self.buyerDict['username']).beSellerFormSubmitted)
        # fill in form and send
        response = c.post("/beSeller", {
            "name": "Goofy Industries",
            "sellerFName": 'goof',
            "sellerLName": 'ball',
            "businessEmail": 'goofball@gmail.com',
            "businessContact": int("02927323122"),
            "identification": int("02927323122"),
            "bio": "keeping it goofy",
            "location": "Goofy street"
        })
        # assert we are rendered a page
        self.assertEqual(200, response.status_code)
        # assert it contains the error message
        self.assertContains(response, "You are not allowed to be here")
        # assert it renders the right page
        self.assertEqual("mySolar/fail.html", response.templates[0].name)
        # assert that no new entries with user of this kind were made
        user = User.objects.get(username=self.sellerDict['username'])
        self.assertEqual(len(sellerRequests.objects.filter(sellerAcc=user)), 0)

    def test_Questions(self):
        # test by getting the questions from database
        que = userQuestions.objects.all()
        # make sure there's only one
        self.assertEqual(len(que), 1)
        # login superuser
        response = c.login(username="king",
                           password="king")
        # check how many questions they receive when they request
        response = c.get("/requestsAndQuestions")
        self.assertContains(response, "Can I get a ")

    def test_QuestionsDeleted(self):
        # delete the question
        # assert that there are no questions
        que = userQuestions.objects.all()
        que.delete()

        que = userQuestions.objects.all()

        self.assertEqual(len(que), 0)

        # login user
        response = c.login(username="king",
                           password="king")

        # check how many questions there are when request
        response = c.get("/requestsAndQuestions")
        self.assertNotContains(response, "Can I get a ")

    def test_CategoryProducts(self):
        """
        categoryProducts for seeing the products in a certain category
            request category
            expect response
            expect certain product
        """
        # assert that we have the product
        self.assertEqual(len(Product.objects.filter(title="solar ting")), 1)
        # send a request for that product category
        response = c.post("/categoryProducts", {
            "category": "MISC"
        })
        # assert we get a proper response
        self.assertEqual(response.status_code, 200)
        # assert that we get the right product
        self.assertContains(response, "solar ting")
        # assert it doesn't contain a product from another category
        self.assertNotContains(response, "solar ting 2")

    def test_CategoryProductsDeleted(self):
        """
        delete product
            request category
            expect response
            expect certain message
        """
        # get the product and delete it
        product = Product.objects.filter(category="MISC")
        product.delete()

        # send a request for that product category
        response = c.post("/categoryProducts", {
            "category": "MISC"
        })
        # assert we get a proper response
        self.assertEqual(response.status_code, 200)
        # assert that we get a "not found" resposne/error
        self.assertContains(
            response, "There are no products in this category yet")
        # assert it doesn't contain a product from another category
        self.assertNotContains(response, "solar ting 2")

    def test_sellerDash_noOrders(self):
        """
        sellerDash for sellers dashboard
            for now
                request sellerDash, expect no orders
        """
        # delete all orders
        delivery_info.objects.all().delete()
        # login our shopkeeper
        c.login(username=self.sellerDict["username"],
                password=self.sellerDict["password"])

        # request to see seller dashboard
        response = c.get("/sellerDash")

        # expect a rendering / 200 OK response
        self.assertEqual(response.status_code, 200)

        # expect no orders
        self.assertContains(response, "You currently do not have any orders")

        # do not expect table showing results on an order to be shown
        self.assertNotContains(response, "Payment Method")

    def test_sellerDash_oneOrder(self):
        """
            add order
            request sellerDash, expect order
                do not expect orders from another person
        """
        # get seller acc
        sellerAcc = User.objects.get(username=self.sellerDict["username"])
        profileAcc = Profile.objects.get(shopkeeper=sellerAcc)
        # get a product
        product = Product.objects.get(title=self.product1Dict['title'])
        # get customer
        buyerAcc = User.objects.get(username=self.buyerDict['username'])
        # add order
        """delivery_info.objects.create(
            seller=profileAcc,
            item=product,
            amount_of_item=1,
            customer=buyerAcc,
            delivery_date=datetime.now(tz=timezone.utc),
            location="123 foo street"
        ) """
        # request the sellerdash as before but this time expecting something
        # login our shopkeeper
        c.login(username=self.sellerDict["username"],
                password=self.sellerDict["password"])

        # request to see seller dashboard
        response = c.get("/sellerDash")

        # expect a rendering / 200 OK response
        self.assertEqual(response.status_code, 200)

        # expect one order
        self.assertContains(response, product.title)
        self.assertContains(response, int("1"))

        # expect no "not found any products" message
        self.assertNotContains(
            response, "You currently do not have any orders")

    def test_one_product(self):
        """
        do not expect a product to exist

        create a proper product
        check if it exists
        """
        product = Product.objects.filter(title="Bottles!")
        self.assertEqual(len(product), 0)

        # create seller
        seller = User.objects.create_user(
            "barry", "barry@gmail.com", "bar", is_shopkeeper=True)

        # create profile linked to seller
        profile = Profile.objects.create(
            shopkeeper=seller, name="bar's shop 1", bio="my shop!",
            location="bar street", how_active=2, identification="1234567890qwr"
        )

        # NOW TO CREATE PRODUCT
        # SIGN IN OUR SHOPKEEPER
        c.login(username="barry",
                password="bar")

        # MAKE A REQUEST TO CREATEPRODUCT PAGE AND CREATE A PRODUCT
        response = c.post("/createProduct", {
            "seller": profile,
            "title": "Bottles!",
            "short_desc": "shorty",
            "long_desc": "longy story shorty",
            "category": "ACC",
            "price": 24,
            "in_stock": True
        })

        # EXPECT RESPONSE STATUS_CODE
        self.assertEqual(response.status_code, 200)

        # EXPECT TO SEE PRODUCT
        product = Product.objects.filter(title="Bottles!")
        self.assertEqual(len(product), 1)

    def test_duplicate_product(self):
        """
        create a duplicate product
        do not expect it to exist
        expect an error
        """
        # create seller
        seller = User.objects.create_user(
            "bazzzy", "bazzzy@gmail.com", "fwooz", is_shopkeeper=True)

        # create profile linked to seller
        profile = Profile.objects.create(
            shopkeeper=seller, name="bar's shop 3", bio="my shop!!!",
            location="bar street", how_active=2, identification="1234567890qwy"
        )

        # SIGN IN OUR SHOPKEEPER
        c.login(username="bazzzy",
                password="fwooz")

        # MAKE A REQUEST TO CREATEPRODUCT PAGE AND CREATE A PRODUCT
        response = c.post("/createProduct", {
            "seller": profile,
            "title": "Cap!",
            "short_desc": "shorty",
            "long_desc": "longy story shorty",
            "category": "ACC",
            "price": 24,
            "in_stock": True
        })

        # EXPECT RESPONSE STATUS_CODE
        self.assertEqual(response.status_code, 200)

        # EXPECT TO SEE PRODUCT
        product = Product.objects.filter(title="Cap!")
        self.assertEqual(len(product), 1)

        # REQUEST AGAIN
        response = c.post("/createProduct", {
            "seller": profile,
            "title": "Cap!",
            "short_desc": "shorty",
            "long_desc": "longy story shorty",
            "category": "ACC",
            "price": 24,
            "in_stock": True
        })
        self.assertContains(
            response, "Product with this Title already exists.")
        self.assertEqual(response.status_code, 200)

    def test_orderInfo_view(self):
        """
        orderInfo for a seller to see and act on orders by buyers
        create an order for a certain seller
        login as that seller
        check for orders

        test action on those orders
            just assert status_codes and certain phrases in those pages or expect certain phrase to not be there
        """
        buyerAcc = User.objects.get(username=self.buyerDict["username"])
        sellerAcc = User.objects.get(username=self.sellerDict["username"])
        profileAcc = Profile.objects.get(shopkeeper=sellerAcc)
        product = Product.objects.get(title=self.product1Dict["title"])

        # assert that the order exists
        orders = delivery_info.objects.filter(
            seller=profileAcc,
            item=product,
            amount_of_item=1
        )
        self.assertEqual(len(orders), 1)

        # login our shopkeeper
        c.login(username=self.sellerDict["username"],
                password=self.sellerDict["password"])

        # act on the order
        # view it first
        response = c.post(f"/orderInfo{orders.first().pk}view")

        # expect to see the page
        self.assertContains(response, orders.first().item.title)
        self.assertEqual(response.status_code, 200)

    def test_orderInfo_process(self):
        sellerAcc = User.objects.get(username=self.sellerDict["username"])
        profileAcc = Profile.objects.get(shopkeeper=sellerAcc)
        product = Product.objects.get(title=self.product1Dict["title"])

        orders = delivery_info.objects.filter(
            seller=profileAcc,
            item=product,
            amount_of_item=1
        )
        # PROCESS
        response = c.post(f"/orderInfo{orders.first().pk}process")

        # expect to see the page
        self.assertContains(
            response, "Item in process or has been completed.")
        self.assertEqual(response.status_code, 200)

        # expect database to say the same
        self.assertTrue(orders.first().processed)

    def test_orderInfo_deliver(self):
        sellerAcc = User.objects.get(username=self.sellerDict["username"])
        profileAcc = Profile.objects.get(shopkeeper=sellerAcc)
        product = Product.objects.get(title=self.product1Dict["title"])

        orders = delivery_info.objects.filter(
            seller=profileAcc,
            item=product,
            amount_of_item=1
        )
        # DELIVER
        response = c.post(f"/orderInfo{orders.first().pk}delivered")

        # expect to see the page
        self.assertContains(
            response, "Item has been delivered.")
        self.assertEqual(response.status_code, 200)

        # expect the database to say the same
        self.assertTrue(orders.first().delivered)

    def test_orderInfo_delete(self):
        sellerAcc = User.objects.get(username=self.sellerDict["username"])
        profileAcc = Profile.objects.get(shopkeeper=sellerAcc)
        product = Product.objects.get(title=self.product1Dict["title"])

        orders = delivery_info.objects.filter(
            seller=profileAcc,
            item=product,
            amount_of_item=1
        )
        # DELETE
        response = c.post(f"/orderInfo{orders.first().pk}delete")

        # expect the database to not find the info
        self.assertEqual(len(orders), 0)

    def test_editProducts(self):
        """
        editProduct for seller to edit existing products                
        expect certain response and check the product for changes
        """
        # get our seller
        seller = Profile.objects.get(name=self.profileDict["name"])
        # get a product
        product = Product.objects.filter(seller=seller).first()
        formerProductTitle = product.title

        # login user
        c.login(username=self.sellerDict["username"],
                password=self.sellerDict["password"])

        # edit the product
        # required fields
        # title, short_desc, long_desc, price
        # change title through request/response
        response = c.post(f"/editProduct{product.pk}edit", {
            "title": "Changed this title",
            "short_desc": product.short_desc,
            "long_desc": product.long_desc,
            "category": product.category,
            "price": product.price
        })
        # send and check response
        """  print(response)
        print("---------------------------------------")
        print(response.content)
        print("---------------------------------------")
        print() """
        # make sure that we are rendered the product page after successful editing
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "mySolar/product.html")

        # make sure the product has been edited successfully by checking the fields that were edited
        self.assertContains(response, "Changed this title")

        # assert the product exists
        # and make sure there are no duplicates!
        newProduct = Product.objects.filter(title="Changed this title")
        self.assertEqual(len(newProduct), 1)

        # assert the other product does not exist
        # and make sure there are no duplicates!
        oldProduct = Product.objects.filter(title=formerProductTitle)
        self.assertEqual(len(oldProduct), 0)

        # make sure that when it is deleted, it ceases to exist, forever
        # send request
        response = c.post(f"/editProduct{newProduct.first().pk}delete")
        # check product database for out product
        newProduct = Product.objects.filter(title="Changed this title")
        self.assertEqual(len(newProduct), 0)

    def editProductsRequiredFields(self, form_error, field, infomation=None):
        """ test that all expected fields are required / filled in """
        """
        for infomation:
            info will be like this:
                {field: value.
                field2: value}

            so we just substitute whatever has been given eg:
                {title: "value"}
        """
        if infomation == None:
            infomation = {}
        # form_error is the error expected
        # field is the name of the field being tested, and that will be sent to the function, eg title
        # infomation is the infomation that must be supplied, eg fields

        # get our seller
        seller = Profile.objects.get(name=self.profileDict["name"])
        # get a product
        product = Product.objects.filter(seller=seller).first()

        # login user
        c.login(username=self.sellerDict["username"],
                password=self.sellerDict["password"])

        # test for field error
        response = self.client.post(
            f"/editProduct{product.pk}edit", infomation)

        self.assertFormError(
            response, 'form', field, form_error)

        # Where "form" is the context variable name for your form, "something" is the field name,
        # and "This field is required." is the exact text of the expected validation error.

    def test_editProductsTitleField(self):
        """ test the title field in the editProducts form """
        # template function: editProductsRequiredFields(self, form_error, field, infomation)

        # it must be present (it is required)
        # no infomation is given meaning that we give an empty post request without the title info
        UserTestCase.editProductsRequiredFields(
            self, "This field is required.", "title", {})

        # and it must be unique
        # edit the title of the product to be the the same as it is now and submit

        # get our seller
        seller = Profile.objects.get(name=self.profileDict["name"])
        # get a product
        product = Product.objects.filter(seller=seller).first()

        infomation = {"title": product.title, }

        # get the product and give that title
        self.editProductsRequiredFields(
            "Product with this Title already exists.", "title", infomation)

        # get another product
        anotherProduct = Product.objects.filter(seller=seller).last()

        # get another product and give that title (it must not only be unique by its own title but by the title of other products)
        self.editProductsRequiredFields("Product with this Title already exists.", "title", {
                                        "title": anotherProduct.title})

    # next is to copy paste most of the function, changing some fields to 'fit' the needs of the different fields. Test only the required fields, declared somewhere up there, and don't forget that for unique fields, test that they both are not the same as the previous title and also another product!
