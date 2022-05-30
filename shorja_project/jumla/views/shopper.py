from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json
from django.db.models import Count
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
    # this an api to add/remove products to cart and create Bills for each shop
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        user_cart = Cart.objects.filter(userOwner=request.user).last()
        get_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=product.shopOwner.id).last()
        # try:
        if get_bill:
            # only add/remove product to the bill And it's already exist
            order_bill_item = get_bill.products.filter(bill_products__products__item=product.id)
            if order_bill_item:
                print("delete")
                item = Bill_Items.objects.filter(bill_products=get_bill).filter(item_id=product.id).first()
                # the bill item exist
                # delete item from bill
                get_bill.products.remove(item)
                get_bill.save()
                item.delete()
            else:
                print("add item")
                # add item to the bill
                bill_items = Bill_Items.objects.create(item_id=product.id)
                bill_items.save()
                get_bill.products.add(bill_items)
                get_bill.save()
        else:
            # create new bill
            bill = Bill.objects.create(total=0, cart_id=user_cart.id, shop_id=product.shopOwner.id)
            bill.save()
            bill_items = Bill_Items.objects.create(item_id=product.id)
            bill_items.save()
            bill.products.add(bill_items)
            bill.save()
    return JsonResponse({'user': {'user_request': request.user.username}, "ali": request.user.username})


def brows_bill(request):
    user_cart = Cart.objects.filter(userOwner=request.user).last()
    cart_bills = Bill.objects.filter(cart_id=user_cart.id)
    context = {'bills': cart_bills}
    return render(request, "jumla/shopper/show_the_bills_ordered.html", context)
