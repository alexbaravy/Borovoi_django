from django.contrib import admin
from django.urls import include, path
from .views import get_products

urlpatterns = [
    path("products/", get_products),


]