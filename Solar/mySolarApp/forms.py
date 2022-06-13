from django import forms
from .models import *
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    class Meta:
        model = User
        exclude = ("first_name", "last_name","groups", "user_permissions", "is_staff", "is_active", "is_superuser", "last_login", "date_joined", "is_shopkeeper")

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ( "name", "desc", "profile_pic", "banner_pic")

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("user", "is_closed", "in_stock", "seller")
class delivery_infoForm(forms.ModelForm):
    class Meta:
        model = delivery_info
        exclude = ("processed", "item", "customer")
