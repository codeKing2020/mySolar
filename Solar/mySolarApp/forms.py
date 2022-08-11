from django import forms
from .models import *


class userProfileForm(forms.ModelForm):
    """Form for changing User values"""
    class Meta:
        model = User
        exclude = (
            "is_active", "beSellerFormSubmitted", "groups",
            "password", "user_permissions", "is_staff",
            "is_superuser", "last_login", "date_joined",
            "is_shopkeeper"
        )


class sellerProfileForm(forms.ModelForm):
    """Form for changing seller info"""
    class Meta:
        model = Profile
        exclude = ("shopkeeper",)


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


class createProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("is_closed", "in_stock", "seller")
        labels = {
            "pic": "Picture of Item"
        }


class delivery_infoForm(forms.ModelForm):
    class Meta:
        model = delivery_info
        exclude = ("processed", "item", "customer", "closed")


class askQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(askQuestionForm, self).__init__(*args, **kwargs)
        self.fields['question'].required = True

    class Meta:
        model = userQuestions
        exclude = ("is_FAQ",)
        labels = {
            "email": "What is your email?",
            "question": "What can we help you with?"
        }
        widgets = {
            "email": forms.TextInput(attrs={'placeholder': 'We will email you our response ASAP.'}),
            "question": forms.Textarea(attrs={'placeholder': 'Ask anything!'})
        }


class categoryProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = {"category"}
