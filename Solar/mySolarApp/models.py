from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    contact_info = models.CharField(max_length=15, blank=True)
    is_shopkeeper = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}: shopkeeper: {self.is_shopkeeper} email: {self.email}'

class Profile(models.Model):
    shopkeeper = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=1000)
    profile_pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='profile_and_banner_images')
    banner_pic = models.ImageField(blank=True, height_field=None, width_field=None, upload_to='profile_and_banner_images')
class Product(models.Model):
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
    # payment methods
    ONPOINT = "On point"
    ONLINE = "Online"

    PAYMENT = [
        (ONPOINT, "On point"),
        (ONLINE, "Online")
    ]

    item = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="product_deliveryInfo")
    amount_of_item = models.IntegerField(null=False, default=1)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="customer_deliveryInfo")
    delivery_date = models.DateTimeField()
    location = models.CharField(max_length=256)
    processed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT, default=ONPOINT)

