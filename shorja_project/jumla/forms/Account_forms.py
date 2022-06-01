from django import forms

from ..models import User


class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField()
    phone_number = forms.CharField(max_length=11)
    Address = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())


class Change_Password(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirmation = forms.CharField(widget=forms.PasswordInput())

