from django.db import models

# Create your models here.
CATEGORY = [
    ("FR", "Fruit"),
    ("MT", "Meat"),
    ("AL", "Alcohol"),
]


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=False, default="Perfect Product")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # vendor = models.CharField(max_length=30)
    amount = models.PositiveIntegerField()
    delivery_date = models.DateField(auto_now_add=True)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY
    )


class Category(models.Model):
    name = models.CharField(max_length=40)


class Vendor(models.Model):
    name = models.CharField(max_length=40)
    foundation_year = models.PositiveIntegerField(null=True)
    country = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)


def __str__(self):
    return self.name
