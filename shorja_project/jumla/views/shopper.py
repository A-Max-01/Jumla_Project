
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ..decorators import *
from ..models import *
from ..utilities import *

# @login_required()
# @allowed_users(allowed_roles=['shopper'])


def home(request):
    #   It displays products to the customer and includes the search process
    #   and includes paginator
    products = Product.objects.all()
    img = Image.objects.all()
    paginator_element = MyPaginator(products, 2)
    page_number = request.GET.get('page')
    page_elements = paginator_element.get_pages(page_number)
    context = {"images": img, "page_elements": page_elements[1], "page_nums": page_elements[0]}
    return render(request, "jumla/shopper/home.html", context)


@csrf_exempt
def add_to_cart(request):
    # this an api to add/remove products to cart
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
    return JsonResponse({'user': {'user_request': request.user.username}, "ali":request.user.username})
