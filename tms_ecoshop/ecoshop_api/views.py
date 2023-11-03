from django.shortcuts import render
from ecoshop.models import Product
# Create your views here.

def get_products(request):
    products = Product.objects.all()[:10]


