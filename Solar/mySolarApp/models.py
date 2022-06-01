from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class store_item(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    pic = models.CharField("Link to picture", max_length=1000)
    short_desc = models.CharField("Short Description", max_length=150)
    long_desc = models.CharField("Long Description", max_length=5000)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title