from django import forms

from ..models import *


class Create_product(forms.ModelForm):
    # ProductName = forms.CharField(label='اسم المنتج',
    #                               widget=forms.TextInput(attrs={
    #                                'class': 'rounded w-96 h-10 bg-gray-200 text-black px-4 py-2'}))
    # Size = forms.CharField(label='القياس',
    #                               widget=forms.TextInput(attrs={
    #                                'class': 'rounded w-96 h-10 bg-gray-200 text-black px-4 py-2'}))
    # price = forms.CharField(label='القياس',
    #                               widget=forms.TextInput(attrs={
    #                                'class': 'rounded w-96 h-10 bg-gray-200 text-black px-4 py-2'}))
    description = forms.CharField(label="الوصف", widget=forms.Textarea(
                        attrs={
                            'cols': '20',
                            'rows': '5',
                            'class': "form-control",
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
