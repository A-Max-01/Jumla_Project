import datetime

from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ..decorators import *
from ..models import *
from ..utilities import *


def home(request):
    #   It displays products to the customer and includes the search process
    #   and includes paginator
    category_get = request.GET.get('category_get')
    product_get = request.GET.get('product_get')
    if product_get:
        product = Product.objects.get(id=product_get)
        return render(request, 'jumla/shopper/card_details.html', {'product': product})
    if category_get:
        category_name = get_object_or_404(Category, name=category_get)
        products = Product.objects.filter(is_active=True, Category=category_name.id)
    else:
        products = Product.objects.filter(is_active=True)

    latest_products = Product.objects.order_by('-Date')[:4]
    random_selected_products = Product.objects.order_by('?')[:4]
    discount = Product.objects.order_by('?')[:4]
    category_get = Category.objects.all()

    paginator_element = MyPaginator(products, 8)
    page_number = request.GET.get('page')
    page_elements = paginator_element.get_pages(page_number)
    context = {"page_elements": page_elements[1], "page_nums": page_elements[0], "cate": category_get,
               'latest_products': latest_products, 'random_selected_products': random_selected_products,
                'discount_products': discount,

               }
    return render(request, "jumla/shopper/home.html", context)


@csrf_exempt
@login_required(login_url='login')
def add_to_cart(request):
    # this an api to add/remove products to cart and create Bills for each shop
    global order_bill_item
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        user_cart = Cart.objects.filter(userOwner=request.user).last()
        # get_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=product.shopOwner.id).last()
        get_bill, created = Bill.objects.get_or_create(cart_id=user_cart.id, shop_id=product.shopOwner.id)
        try:
            # delete item from bill
            order_bill_item = get_bill.products.get(item_id=product.id)
            get_bill.products.remove(order_bill_item)
            order_bill_item.delete()
        except Bill_Items.DoesNotExist:
            # create an item and added to bill items
            bill_items = Bill_Items.objects.create(item_id=product.id)
            bill_items.save()
            get_bill.products.add(bill_items)
        get_bill.get_total()
        return JsonResponse({'bill_total': get_bill.get_total(),
                             'cart_total': user_cart.get_cart_total(),
                             })
    return JsonResponse({'Get': 'the api worked'})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def show_cart_bills_order(request):
    # this api to send all order bills in user cart
    # and if the order bill has not any products will delete it
    cities = Governorate.objects.all()
    user_cart = Cart.objects.filter(userOwner=request.user).last()
    cart_bills = Bill.objects.filter(cart_id=user_cart.id)
    user_cart.total = user_cart.get_cart_total()
    bills_not_have_products = [result for shop in cart_bills.filter(total=0).values('shop') for result in shop.values()]
    for shop_id in bills_not_have_products:
        get_order_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=shop_id)
        get_order_bill.delete()
    for bill in cart_bills:
        bill.total = bill.get_total()
        # POST Method for checkout
    if request.method == "POST":
        # check for bills.total == 0 then delete it
        # create new cart for request.user
        if user_cart.total == 0:
            # if user current cart no have any bills than redirect to home to Buy some products
            return redirect('home')
        else:
            # else check for bills and create new cart
            for shop_id in bills_not_have_products:
                get_order_bill = Bill.objects.filter(cart_id=user_cart.id, shop_id=shop_id)
                get_order_bill.delete()
            try:
                city = request.POST.get('city')
                user_cart.checkout = True
                user_cart.city_id = city
                user_cart.save()
                cart = Cart.objects.create(userOwner_id=request.user.id)
                cart.save()
                return redirect('home')
            except:
                return redirect('brows_bills')
    context = {'bills': cart_bills,
               'cities': cities,
               'user_cart': user_cart
               }
    return render(request, "jumla/shopper/show_the_bills_ordered.html", context)


@csrf_exempt
@login_required(login_url='login')
def check_item_in_bill_order(request):
    # this api to send products in each bill in the cart
    user_cart = Cart.objects.filter(userOwner=request.user).last()
    cart_bills = Bill.objects.filter(cart_id=user_cart.id)
    products_bill_order = cart_bills.values('products__item')
    items_in_cart = [result for item in products_bill_order for result in item.values()]
    return JsonResponse({'items_in_cart': items_in_cart})


@csrf_exempt
@login_required(login_url='login')
def update_quentity(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        one_img = product.Image_Product
        print(one_img)
        qty = data.get('qty')
        user_cart = Cart.objects.filter(userOwner=request.user).last()
        get_bill = Bill.objects.filter(cart__userOwner_id=request.user.id, shop_id=product.shopOwner.id).last()
        if get_bill:
            item = Bill_Items.objects.filter(bill_products=get_bill).filter(item_id=product.id).first()
            if item:
                item.qty = qty
                item.save()
                return JsonResponse({'bill_total': get_bill.get_total(),
                                     'cart_total': user_cart.get_cart_total(),
                                     })
    return JsonResponse({'Get': 'the api worked'})


def who(request):
    return render(request, "jumla/base/who.html")
