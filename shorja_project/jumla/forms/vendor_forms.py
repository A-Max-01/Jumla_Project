from django import forms

from ..models import *


class Create_product(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "ProductName",
            'Size',
            'price',
            'description',
            'Category'
        ]

