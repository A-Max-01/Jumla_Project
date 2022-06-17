
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
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


@unauthenticated_user
def register_view(request):
    if request.method == "POST":
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('Address')
        first_name = request.POST.get('username')
        confirmation = request.POST.get('confirmation')
        if password != confirmation:
            return render(request, "jumla/Account/register.html", {
                "message": "Passwords must match."
            })
        try:
            group = Group.objects.get(name='customer')
            user = User.objects.create_user(phone_number, first_name, address, password)
            user.groups.add(group)
            user.save()
            # to create cart for this user to first time
            cart = Cart.objects.create(userOwner_id=user.id)
            cart.save()
        except IntegrityError as e:
            print(e)
            return render(request, "jumla/Account/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return redirect("home")
    context = {}
    return render(request, "jumla/Account/register.html", context)


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user:
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, "jumla/Account/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('home')


def change_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password and confirmation:
            if password != confirmation:
                return render(request, "jumla/Account/register.html", {
                    "message": "Passwords must match."
                })
            request.user.password = make_password(password)
            request.user.save()
            logout(request)
            return redirect('login')
    context = {'user': request.user}
    return render(request, "jumla/Account/change_password.html", context)
