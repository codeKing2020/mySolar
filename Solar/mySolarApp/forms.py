from django import forms
from .models import store_item

class storeItemForm(forms.ModelForm):

    class Meta:
        model = store_item
        exclude = ("user", )