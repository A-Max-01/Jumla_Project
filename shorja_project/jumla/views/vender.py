import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ..decorators import *
from ..forms import *
from ..models import *
from ..utilities import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['vendor'])
def vendor_home(request):
    shop = get_object_or_404(Shop, shopOwner_id=request.user.id)
    shop_products = Product.objects.filter(shopOwner_id=shop.id)
    q = request.GET.get('q')
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
    paginator_element = MyPaginator(shop_products, 10)
    page_number = request.GET.get('page')
    page_elements = paginator_element.get_pages(page_number)

    context = {"page_elements": page_elements[1], "page_nums": page_elements[0]}
    return render(request, "jumla/vender/home.html", context)


@csrf_exempt
@login_required(login_url='login')
def delete_product_and_update_is_active(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        operation_type = data.get('type')
        if product:
            if operation_type == 'delete_image':
                image_url = data.get('image_url')
                product_images = product_Images.objects.filter(product_id=product.id)
                if product_images:
                    for i in product_images:
                        if i.image.url == image_url:
                            path = i.image.path
                            i.image.storage.delete(path)
                            i.delete()
                return JsonResponse({"PUT": "delete image done"})
            if operation_type == "delete":
                # to delete a product that must delete it images form media folder
                product_images = product_Images.objects.filter(product_id=product.id)
                if product_images:
                    for i in product_images:
                        path = i.image.path
                        i.image.storage.delete(path)
                product.delete()
                return JsonResponse({"PUT": "delete ok"})
            elif operation_type == "update_checkbox":
                if product.is_active:
                    product.is_active = False
                else:
                    product.is_active = True
                product.save()
                return JsonResponse({"PUT": "checkbox updated ok"})
    return JsonResponse({"Get": "this api is worked"})


@login_required(login_url='login')
# @allowed_users(allowed_roles=['vendor'])
def create_new_product(request):
    categories = Category.objects.all()
    form = vendor_forms.Create_product()
    if request.method == "POST":
        form = vendor_forms.Create_product(request.POST)
        if form.is_valid():
            files = request.FILES.getlist('files')
            product_name = form.cleaned_data['ProductName']
            product_size = form.cleaned_data['Size']
            category = form.cleaned_data['Category']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            shop = get_object_or_404(Shop, shopOwner_id=request.user.id)
            if shop:
                create_product = Product.objects.create(ProductName=product_name, shopOwner_id=shop.id,
                                                        Size=product_size, Category_id=category.id, price=price,
                                                        description=description)
                create_product.save()
                if files:
                    for file in files:
                        image_product = product_Images.objects.create(product_id=create_product.id, image=file)
                        image_product.save()
                    return redirect('vendor_home')
        else:
            return redirect('create_product')
    context = {'categories': categories,
               'form': form}
    return render(request, 'jumla/vender/adding_products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['vendor'])
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    img = product_Images.objects.all()
    form = vendor_forms.Create_product(instance=product)
    if request.method == "PUT":
        return HttpResponse('Put')
    if request.method == "POST":
        images = request.FILES.getlist('files')
        form = vendor_forms.Create_product(request.POST, instance=product)
        if form.is_valid():
            form.save()
            if images:
                for image in images:
                    image_product = product_Images.objects.create(product_id=product.id, image=image)
                    image_product.save()
        return redirect('vendor_home')
    context = {'product': product,
               "images": img,
               'form': form,
               }
    return render(request, "jumla/vender/editing_product.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['vendor'])
def view_customer_bills(request):
    bills = Bill.objects.filter(cart__checkout=True, shop__shopOwner_id=request.user.id)
    for bill in bills:
        bill.total = bill.get_total()
        print(bill.total)
        if bill.total == 0:
            bill.delete()

    paginator_element = MyPaginator(bills, 10)
    page_number = request.GET.get('page')
    page_elements = paginator_element.get_pages(page_number)

    context = {"page_elements": page_elements[1], "page_nums": page_elements[0]}
    return render(request, 'jumla/vender/view_customer_bills.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['vendor'])
def view_bill_products(request, bill_id):
    # bill = get_object_or_404(Bill, id=bill_id)
    bill = Bill.objects.filter(id=bill_id).first()
    context = {'bill_products': bill.products.all()}
    return render(request, 'jumla/vender/view_bill_products.html', context)


def show_store(request, store):
    vender = get_object_or_404(Shop, shopName__contains=store)
    shop_products = Product.objects.filter(shopOwner__shopName__contains=vender)
    paginator_element = MyPaginator(shop_products, 10)
    page_number = request.GET.get('page')
    page_elements = paginator_element.get_pages(page_number)

    context = {"page_elements": page_elements[1], "page_nums": page_elements[0], 'vender': vender}
    return render(request, 'jumla/vender/stores.html', context)
