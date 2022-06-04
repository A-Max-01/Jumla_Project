
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
# @login_required()
def home(request):
    #   It displays products to the customer and includes the search process
    #   and includes paginator
    products = Product.objects.all()
    img = product_Images.objects.all()
    paginator_element = MyPaginator(products, 2)
    page_number = request.GET.get('page')
    page_elements = paginator_element.get_pages(page_number)
    context = {"images": img, "page_elements": page_elements[1], "page_nums": page_elements[0]}
    return render(request, "jumla/shopper/home.html", context)


@csrf_exempt
# @login_required()
def add_to_cart(request):
    # this an api to add/remove products to cart and create Bills for each shop
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        user_cart = Cart.objects.filter(userOwner=request.user).last()
        get_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=product.shopOwner.id).last()
        if get_bill:
            # only add/remove product to the bill And it's already exist
            order_bill_item = get_bill.products.filter(bill_products__products__item=product.id)
            if order_bill_item:
                # print("delete")
                # the bill item exist
                # delete item from bill
                item = Bill_Items.objects.filter(bill_products=get_bill).filter(item_id=product.id).first()
                get_bill.products.remove(item)
                get_bill.save()
                item.delete()
            else:
                # print("add item")
                # add item to the bill
                bill_items = Bill_Items.objects.create(item_id=product.id)
                bill_items.save()
                get_bill.products.add(bill_items)
                get_bill.save()
        else:
            # create new bill
            bill = Bill.objects.create(total=0, cart_id=user_cart.id, shop_id=product.shopOwner.id)
            # bill.total = bill.get_total
            bill.save()
            bill_items = Bill_Items.objects.create(item_id=product.id)
            bill_items.save()
            bill.products.add(bill_items)
            bill.save()
        get_bill.total = get_bill.get_total
        return JsonResponse({'total': get_bill.get_total})
    # {'user_request': request.user.first_name}
    return JsonResponse({'Get': 'the api worked'})


def show_cart_bills_order(request):
    # this api to send all order bills in user cart
    # and if the order bill has not any products will delete it
    user_cart = Cart.objects.filter(userOwner=request.user).last()
    cart_bills = Bill.objects.filter(cart_id=user_cart.id)
    shop_list_id = [result for shop in cart_bills.filter(products__item=None).values('shop') for result in shop.values()]
    for shop_id in shop_list_id:
        get_order_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=shop_id)
        get_order_bill.delete()
    for bill in cart_bills:
        bill.total = bill.get_total
        bill.save()
    context = {'bills': cart_bills}
    return render(request, "jumla/shopper/show_the_bills_ordered.html", context)


@csrf_exempt
def check_item_in_bill_order(request):
    # this api to send products in each bill in the cart
    user_cart = Cart.objects.filter(userOwner=request.user).last()
    cart_bills = Bill.objects.filter(cart_id=user_cart.id)
    products_bill_order = cart_bills.values('products__item')
    items_in_cart = [result for item in products_bill_order for result in item.values()]
    return JsonResponse({'items_in_cart': items_in_cart})


@csrf_exempt
def update_quentity(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        qty = data.get('qty')
        user_cart = Cart.objects.filter(userOwner=request.user).last()
        get_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=product.shopOwner.id).last()
        if get_bill:
            # order_bill_item = get_bill.products.filter(bill_products__products__item=product.id)
            item = Bill_Items.objects.filter(bill_products=get_bill).filter(item_id=product.id).first()
            if item:
                item.qty = qty
                item.save()
                return JsonResponse({'total': get_bill.get_total})
    return JsonResponse({'Get': 'the api worked'})
