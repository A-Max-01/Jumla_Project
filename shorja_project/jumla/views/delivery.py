from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from ..decorators import *
from ..models import *
from ..utilities import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['delivery', 'admin'])
def home(request):
    get_city = request.GET.get('city')
    print(get_city)
    cities = Governorate.objects.all()
    carts = Cart.objects.filter(checkout=True)
    for cart in carts:
        cart.get_cart_total()
        if cart.total == 0:
            cart.delete()
    paging_carts = MyPaginator(carts, 10)
    page_number = request.GET.get('page')
    page_carts = paging_carts.get_pages(page_number)
    context = {'cities': cities,
               'page_elements': page_carts[1],
               'page_nums': page_carts[0],
               }
    return render(request, "jumla/delivery/noor'sversion/costumers_delivery.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['delivery', 'admin'])
def get_cart_bills(request, cart_id):
    cart_bills = Bill.objects.filter(cart_id=cart_id)
    paging_bills = MyPaginator(cart_bills, 10)
    page_number = request.GET.get('page')
    page_bills = paging_bills.get_pages(page_number)
    context = {
        'page_elements': page_bills[1],
        'page_nums': page_bills[0],
    }
    return render(request, "jumla/delivery/noor'sversion/customer_basket.html", context)

