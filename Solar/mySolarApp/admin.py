from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(delivery_info)
admin.site.register(sellerRequests)
admin.site.register(userQuestions)
