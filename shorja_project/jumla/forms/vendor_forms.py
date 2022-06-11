from django import forms

from ..models import *


class Create_product(forms.ModelForm):

    description = forms.CharField(label="الوصف", widget=forms.Textarea(
                        attrs={
                            'cols': '20',
                            'rows': '5',
                            'class': 'form-control',
                            'placeholder': "الوصف",
                        }), required=True,)

    class Meta:
        model = Product
        fields = [
            'ProductName',
            'Size',
            'price',
            'description',
            'Category',
        ]
        labels = {
            'Category': "الصنف",
            'price': 'السعر',
            'Size': "القياس",
            'ProductName': 'اسم المنتج'
        }
