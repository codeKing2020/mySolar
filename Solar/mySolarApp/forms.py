from django import forms
from .models import *


class SellerRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SellerRequestForm, self).__init__(*args, **kwargs)
        self.fields['sellerFName'].required = True
        self.fields['sellerLName'].required = True
        self.fields['businessEmail'].required = True
        self.fields['businessContact'].required = True
        self.fields['sellerAcc'].required = False

    class Meta:
        model = sellerRequests
        fields = "__all__"
        labels = {
            "sellerFName": "First Name of Business Owner",
            "sellerLName": "Last Name of Business Owner",
            "businessEmail": "Email Address of Business",
            "businessContact": "Business contact info",
            "name": "Name of Company",
            "location": "Location of Company",
            "profile_pic": "Profile Picture",
            "banner_pic": "Banner Picture",
            "how_active": "How active will you be each week?",
            "identification": "Identification number"
        }
        widgets = {
            "sellerAcc": forms.HiddenInput(),
            "how_active": forms.NumberInput(attrs={'min': '1', 'max': '7', 'step': '1'})
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("user", "is_closed", "in_stock", "seller")


class delivery_infoForm(forms.ModelForm):
    class Meta:
        model = delivery_info
        exclude = ("processed", "item", "customer")


class askQuestionForm(forms.ModelForm):
    class Meta:
        model = help
        exclude = ("is_FAQ",)
        labels = {
            "question": "What can we help you with?"
        }
        widgets = {
            "question": forms.Textarea(attrs={'placeholder': 'Ask anything!'})
        }
