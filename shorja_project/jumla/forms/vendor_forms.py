from django import forms
from crispy_forms.helper import FormHelper
from ..models import *


class Create_product(forms.ModelForm):
    ProductName = forms.CharField(label='اسم المنتج',
                                   widget=forms.TextInput(attrs={
                                    'class': '  shadow mr-4 rounded  h-10 bg-white  focus:outline-none text-black  px-4 py-1'}))
    Size = forms.CharField(label='القياس',
                                   widget=forms.TextInput(attrs={
                                    'class': ' mr-8   shadow rounded  h-10 bg-white  focus:outline-none text-black  px-4 py-1'}))
    price = forms.CharField(label='السعر',
                                  widget=forms.TextInput(attrs={
                                   'class': ' mr-10 rounded  shadow  h-10 bg-white  focus:outline-none text-black  px-4 py-1'}))
    description = forms.CharField(label="الوصف", widget=forms.Textarea(
                        attrs={
                            'cols': '20',
                            'rows': '5',
                            'class': "mr-5  shadow rounded w-72",
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
    def __init__(self, *args, **kwargs):
        super(Create_product, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False