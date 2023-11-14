from django.contrib import admin
from django.urls import include, path
from .views import CustomerDetails, ProductCustomers, ProductsList, ProductDetails, ProductsListGeneric, \
    ProductDetailsGeneric, VendorsList, VendorDetails, VendorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vendors-view-set', VendorViewSet, basename='vendor')

urlpatterns = [
    path("customer-details/<int:pk>", CustomerDetails.as_view(), name='customer-details'),

    path("products/", ProductsList.as_view(), name='products'),
    path("product-details/<int:pk>", ProductDetails.as_view(), name='product-details'),

    path("product-customers/<int:pk>", ProductCustomers.as_view(), name='product-customers'),

    path("products-generics/", ProductsListGeneric.as_view(), name='products-generics'),
    path("product-generics-details/<int:pk>", ProductDetailsGeneric.as_view(), name='product-generics-details'),

    path("vendors/", VendorsList.as_view(), name='vendors'),
    path("vendor-details/<int:pk>", VendorDetails.as_view(), name='vendor-details'),
    path('', include(router.urls)),

]
