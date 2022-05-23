from django.shortcuts import render
from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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


def register_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {'form': form}
    return render(request, "jumla/Account/register.html", context)


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], passowrd=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
    context = {'form': form}
    return render(request, "jumla/Account/login.html", context)



