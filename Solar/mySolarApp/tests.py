from django.test import TestCase
from mySolarApp.models import *
# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):
        # Create Simple User
        user = User.objects.create(
            first_name="Tavonga",
            last_name="Lewis",
            username="foo",
            email="lewistavonga@gmail.com",
            password="foo",
        )

        # Create Shopkeeper
        shopkeeper = User.objects.create(
            first_name="Shop",
            last_name="Keeper",
            username="shopkeeper",
            email="shopkeeper@gmail.com",
            password="shopkeeper"
        )

        profile = Profile.objects.create(
            shopkeeper = shopkeeper,
            name = "Foo",
            desc="bar"
        )

        # Create Bad User
        badUser = User.objects.create(
            username="baz",
            email="baz",
        )

    def test_valid_User(self):
        f = User.objects.get(username="foo")


