
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=255, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Governorate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Shop(models.Model):
    shopName = models.CharField(max_length=255)
    shopOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shopOwner")

    def __str__(self):
        return f"{self.shopName}"


class Product(models.Model):
    ProductName = models.CharField(max_length=255)
    Size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    shopOwner = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_products")
    Date = models.DateTimeField(default=timezone.now)
    Available = models.BooleanField(default=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_Category")

    def __str__(self):
        return f"{self.ProductName} ,  {self.Category}"


class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Image_Product")

    def __str__(self):
        return f"{self.product}"


class Cart(models.Model):
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    Date = models.DateTimeField()
    Governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name="cart_Governorate")

    def __str__(self):
        return f" {self.userOwner}, {self.Governorate}"


class Bill_Items(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_item")
    qty = models.IntegerField('item_qty')


class Bill(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="bill_cart")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_bill")
    products = models.ManyToManyField(Bill_Items, related_name="bill_products")
    Date = models.DateTimeField()
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f" {self.cart},  {self.shop}"
