from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    User Model
    
    Stores info about EVERY user, including the shopkeepers and the admin
    Valuable fields in here:
        username
        first_name
        last_name
        email
        password
        beSellerFormSubmitted

        useful information regarding this model can be found at https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User
        including info about getting full name or changing password etc
    """
    beSellerFormSubmitted = models.BooleanField(default=False)
    contact_info = models.CharField(max_length=15, blank=True)
    is_shopkeeper = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}: shopkeeper: {self.is_shopkeeper} email: {self.email}'

# "contact_info", "location", "how_active", "ID"
class Profile(models.Model):
    """
    Profile model

    For shopkeepers only!
    links to user model and stores:
        name of company
        bio of company
        profile picture and banner picture
        location of store
        how active they'll be per week (could be useful later for search optimisation)
        identification number of shop owner for authenticity
    """
    shopkeeper = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    bio = models.CharField(max_length=1000)
    profile_pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='profile_and_banner_images')
    banner_pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='profile_and_banner_images')
    location = models.CharField(max_length=128)
    how_active = models.IntegerField()
    identification = models.CharField(max_length=13)

class Product(models.Model):
    """
    Product model

    stores info about products
    stores info about seller
    has title and picture of item (could later change it to accomodate multiple pictures)
    short and long description of the product (one is to be seen on the store page, the other is visible on the moreInfo about product page)
    stores the product in a category for search optimization
    has fields to check if it is still in stock or is closed (in the case that someone tries to access it and they try to buy an item thats closed)
    """
    # Categories - choices
    SLP = "SLP" # solar panels
    BAT = "BAT" # batteries
    INV = "INV" # inverters
    CHA_CTRL = "CHA_CTRL" # charge controllers 
    WAT_PUMPS = "WAT_PUMPS" # water pumps
    ACC = "ACC" # accessories
    TOOLS = "TOOLS" # tools
    MISC = "MISC" # miscellaneous 
    

    CATEGORY = [
        (SLP, "Solar Panels"),
        (BAT, "Batteries"),
        (INV, "Inverters"),
        (CHA_CTRL, "Charge Controllers"),
        (WAT_PUMPS, "Water Pumps"),
        (ACC, "Accessories"),
        (TOOLS, "Tools"),
        (MISC, "Miscellaneous/Other"),
    ]

    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="product_seller")
    title = models.CharField(max_length=64)
    pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='product_images')
    short_desc = models.CharField("Short Description", max_length=150)
    long_desc = models.CharField("Long Description", max_length=5000)
    category = models.CharField(max_length=10, choices=CATEGORY, default=MISC)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True) 
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} instock: {self.in_stock} sold by {self.seller} for {self.price} in the {self.category} category, isclosed: {self.is_closed}'

class delivery_info(models.Model):
    """
    delivery_info model

    where info about a product a person bought is stored
    stores: 
        item itself
        the amount of the item (say five solar panels)
        the customer
        the delivery date set by the customer, could later be changed by the seller and then notifies the customer
        the location of the customer
        whether it has been processed or not
        payment method that the customer has chosen
    """
    # payment methods
    ONPOINT = "On point"
    ONLINE = "Online"

    PAYMENT = [
        (ONPOINT, "On point"),
        (ONLINE, "Online")
    ]

    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_deliveryInfo")
    amount_of_item = models.IntegerField(null=False, default=1)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_deliveryInfo")
    delivery_date = models.DateTimeField(verbose_name=("Delivery Date"), auto_now_add=False, null=False, blank=False)
    location = models.CharField(max_length=128)
    processed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT, default=ONPOINT)


class sellerRequests(models.Model):
    """
    sellerRequests model

    stores info about users who have requested to sell but are not yet authorised
    once authorised, their info must be allocated to new fields in the system and then this field is deleted
    """
    sellerAcc = models.ForeignKey(User, on_delete=models.CASCADE)
    sellerFName = models.CharField(max_length=24, blank=False)
    sellerLName = models.CharField(max_length=24, blank=False)
    businessEmail = models.EmailField(blank=False)
    businessContact = models.CharField(max_length=15, blank=False)
    name = models.CharField(max_length=64, unique=True, blank=False)
    location = models.CharField(max_length=128, blank=False)
    bio = models.CharField(max_length=1000, blank=False)
    profile_pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='profile_and_banner_images')
    banner_pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='profile_and_banner_images')
    how_active = models.IntegerField()
    identification = models.CharField(max_length=13, unique=True, blank=False)

class userQuestions(models.Model):
    """
    help model 

    for storing any questions asked by users
    takes email also
    also stores FAQs which are saved and accessed by page
    """
    email = models.EmailField(blank=True)
    question = models.CharField(max_length=1000, blank=False, unique=True)
    is_FAQ = models.BooleanField(default=False)