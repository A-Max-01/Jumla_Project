
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ..decorators import *
from ..models import *
from ..utilities import *


@allowed_users(allowed_roles=['vendor'])
def vendor_home(request):
    shop = get_object_or_404(Shop, shopOwner_id=request.user.id)
    shop_products = Product.objects.filter(shopOwner_id=shop.id)
    q = request.GET.get('q')
    print(q)
    if q:
        try:
            q = int(q)
            shop_products = shop_products.filter(
                Q(price__lte=q)

            )
        except:
            shop_products = shop_products.filter(
                Q(ProductName__icontains=q) |
                Q(Category__name__icontains=q) |
                Q(Category__parent__name__icontains=q)
            )
    context = {'products': shop_products,
               'user_group': request.user.groups.all()[0].name
               }
    return render(request, "jumla/vender/home.html", context)


@csrf_exempt
def delete_product_and_update_is_active(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        type = data.get('type')
        if product:
            if type == "delete":
                # to delete a product that must delete it images form media folder
                product_images = product_Images.objects.filter(product_id=product.id)
                if product_images:
                    for i in product_images:
                        path = i.image.path
                        i.image.storage.delete(path)
                product.delete()
                return JsonResponse({"PUT": "delete ok"})
            elif type == "update_checkbox":
                if product.is_active:
                    product.is_active = False
                else:
                    product.is_active = True
                product.save()
                return JsonResponse({"PUT": "checkbox updated ok"})
    return JsonResponse({"Get": "this api is worked"})


def create_new_product(request):
    categories = Category.objects.all()
    if request.method == "POST":
        files = request.FILES.getlist('files')
        product_name = request.POST.get('product_name')
        product_size = request.POST.get('product_size')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if product_name and product_size and category and price and description and files:
            shop = get_object_or_404(Shop, shopOwner_id=request.user.id)
            if shop:
                product = Product.objects.create(ProductName=product_name, shopOwner_id=shop.id, Size=product_size,
                                                 Category_id=category, price=price, description=description)
                product.save()
                for file in files:
                    image_product = product_Images.objects.create(product_id=product.id, image=file)
                    image_product.save()
                return redirect('vendor_home')
        else:
            return redirect('create_product')
    context = {'categories': categories}
    return render(request, 'jumla/vender/adding_products.html', context)


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    img = product_Images.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_size = request.POST.get('product_size')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        if product:
            product.ProductName = product_name
            product.Size = product_size
            product.Category_id = category
            product.price = price
            product.description = description
            product.Date = timezone.now()
            product.save()
        return redirect('vendor_home')
    context = {'product': product,
               "images": img,
               'categories': categories}
    return render(request, "jumla/vender/editing_product.html", context)


def view_customer_bills(request):
    bills = Bill.objects.filter(cart__checkout=True, shop__shopOwner_id=request.user.id)
    for bill in bills:
        bill.total = bill.get_total
        if bill.total == 0:
            bill.delete()
    context = {'bills': bills}
    return render(request, 'jumla/vender/view_customer_bills.html', context)


def view_bill_products(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    context = {'bill_products': bill.products.all()}
    return render(request, 'jumla/vender/view_bill_products.html',context)
