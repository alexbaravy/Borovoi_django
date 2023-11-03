from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='Wrong')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=16)


class Vendor(User):
    inn = models.CharField(max_length=12, null=True)
    products = models.ManyToManyField("Product")
    def __str__(self):
        return self.name


class Customer(User):
    discount = models.FloatField(default=0)
    products = models.ManyToManyField("Product")

    def __str__(self):
        return self.name


class Passport(models.Model):
    customer = models.OneToOneField("Customer", on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=10)
    passport_series = models.CharField(max_length=10)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 11)]
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class ProductReview(Review):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    author = models.ForeignKey("Customer", on_delete=models.CASCADE)

    class Meta:
        db_table = 'ecoshop_product_reviews'

    def __str__(self):
        return self.title


class VendorReview(Review):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    author = models.ForeignKey("Customer", on_delete=models.CASCADE)

    class Meta:
        db_table = 'ecoshop_vendor_reviews'

    def __str__(self):
        return self.title


class CustomerReview(Review):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    author = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    class Meta:
        db_table = 'ecoshop_customer_reviews'


    def __str__(self):
        return self.title
