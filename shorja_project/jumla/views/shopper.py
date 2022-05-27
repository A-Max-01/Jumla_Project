
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
from ..decorators import *
# from ..models import Category, Cart, Product
# from jumla.models import Category
# from
# @login_required()
# @allowed_users(allowed_roles=['shopper'])
from ..models import *


def home(request):
    #   It displays products to the customer and includes the search process
    #   and includes paginator

    products = Product.objects.all()
    cart = Category.objects.filter()
    return render(request, "jumla/shopper/home.html", {"products": products})
