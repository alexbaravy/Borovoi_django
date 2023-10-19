from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    inn = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Passport(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=10)
    passport_series = models.CharField(max_length=10)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendors = models.ManyToManyField(Vendor)
    customers = models.ManyToManyField(Customer)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)


class VendorRating(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 11)]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'ecoshop_vendor_rating'


class CustomerRating(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 11)]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    author = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'ecoshop_customer_rating'
