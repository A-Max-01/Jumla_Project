
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from ..decorators import *
from ..forms import *
from ..models import *



def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            phone_number = form.cleaned_data.get('phone_number')
            Address = form.cleaned_data.get('Address')
            username = form.cleaned_data.get('username')
            confirmation = form.cleaned_data.get('confirmation')
            if password != confirmation:
                return render(request, "jumla/Account/register.html", {
                    "message": "Passwords must match."
                })
            try:
                user = User.objects.create(username=username, phone_number=phone_number, address=Address)
                user.password = make_password(password)
                user.save()
                # to create cart for this user to first time
                print(user.id)
                cart = Cart.objects.create(userOwner_id=user.id)
                cart.save()
            except IntegrityError as e:
                print(e)
                return render(request, "jumla/Account/register.html", {
                    "message": "Email address already taken."
                })
            login(request, user)
            return redirect("home")
    context = {'form': form}
    return render(request, "jumla/Account/register.html", context)


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    context = {'form': form}
    return render(request, "jumla/Account/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('home')


def change_password(request):
    form = Change_Password()
    if request.method == "POST":
        form = Change_Password(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('new_password')
            confirmation = form.cleaned_data.get('confirmation')
            if password != confirmation:
                return render(request, "jumla/Account/register.html", {
                    "message": "Passwords must match."
                })
            request.user.password = make_password(password)
            request.user.save()
            return redirect('login')
    context = {'form': form,
               'user': request.user}
    return render(request, "jumla/Account/change_password.html", context)
