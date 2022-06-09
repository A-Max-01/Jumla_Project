from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_number, first_name, address, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone_number:
            raise ValueError('The given email must be set')
        # email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, first_name=first_name, address=address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, first_name, address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, first_name, address, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=255, null=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Category(models.Model):
    parent = models.ForeignKey('self',
                               verbose_name='parent',
                               related_name='children',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/", null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    @property
    def children(self):
        return self.children

    def __str__(self):
        if self.parent:
            return f'-   {self.name}'
        return f'{self.name}'


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
    is_active = models.BooleanField(default=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_Category")

    def __str__(self):
        return f"{self.ProductName} ,  {self.Category}"


class product_Images(models.Model):
    image = models.ImageField(upload_to="images/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Image_Product")

    class Meta:
        verbose_name = "product_Image"
        verbose_name_plural = "product_Images"

    def __str__(self):
        return f"{self.product}"


class Cart(models.Model):
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    Date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True)
    checkout = models.BooleanField(default=False, null=True)
    city = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name="cart_city", null=True)

    def __str__(self):
        return f"cart user :  {self.userOwner}"

    def get_cart_total(self):
        bills = Bill.objects.filter(cart_id=self.id)
        self.total = sum(b.total for b in bills)
        self.save()
        return self.total


class Bill_Items(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_item")
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.item.id}'


class Bill(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="bill_cart")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_bill")
    products = models.ManyToManyField(Bill_Items, related_name="bill_products")
    Date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f" {self.cart},  {self.shop}"

    @property
    def get_total(self):
        self.total = sum(i.item.price * i.qty for i in self.products.all())
        self.save()
        return self.total

    def serialize(self):
        return{
            "cart": self.cart,
            'vendor': self.shop,
            'products': [p for p in self.products.all()]
        }
