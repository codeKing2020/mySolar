from django import forms
from .models import Product

class storeItemForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("user", )