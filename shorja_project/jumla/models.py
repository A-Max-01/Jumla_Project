import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# المستخدم



class User(AbstractUser):
    phone_number = models.CharField(max_length=11)

# الفئات


class Category(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

# المحافظة


class Governorate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

# المحل


class Shop(models.Model):
    shopName = models.CharField(max_length=255)
    shopOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shopOwner")

    def __str__(self):
        return f"{self.shopName}"


# المنتجات


class Product(models.Model):
    ProductName = models.CharField(max_length=255)
    Size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    shopOwner = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_products")
    Date = models.DateTimeField(default=datetime.datetime.now())
    Available = models.BooleanField(default=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_Category")

    def __str__(self):
        return f"{self.ProductName} ,  {self.Category}"

# لكل منتج اكثر من صورة


class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Image_Product")

    def __str__(self):
        return f"{self.product}"


# سلة الزيون


class Cart(models.Model):
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    Date = models.DateTimeField(default=datetime.datetime.now())
    Governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name="cart_Governorate")

    def __str__(self):
        return f" {self.userOwner}, {self.Governorate}"

# الفاتورة


class Bill(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="bill_cart")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_bill")
    products = models.ManyToManyField(Product, related_name="bill_products")
    Date = models.DateTimeField(default=datetime.datetime.now())
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f" {self.cart},  {self.shop}"

