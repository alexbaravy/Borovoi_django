from django.shortcuts import render, HttpResponse
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, viewsets

from django.http import Http404
from ecoshop.models import Customer, CustomerReview, Product, Vendor
from ecoshop_api.serializers import CustomerDetailsSerializer, ProductCustomersSerializer, ProductSerializer, \
    ProductSerializerGeneric, \
    VendorSerializer
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, Max, ExpressionWrapper, FloatField, Avg, Subquery, F, Sum, Prefetch
from .pagination import LargeResultsSetPagination, StandardResultsSetPagination


class ProductsList(APIView):
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # http://127.0.0.1:8000/api/v1/products/?search=19.99&ordering=amount&category=3
    filterset_fields = ['name', 'price', 'category']
    search_fields = ['name', 'price']
    ordering_fields = ['name', 'price', 'category', 'amount']
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        products = Product.objects.all()
        products = self.filter_backends[0]().filter_queryset(request, products, self)
        products = self.filter_backends[1]().filter_queryset(request, products, self)
        products = self.filter_backends[2]().filter_queryset(request, products, self)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(products, request)
        # import pdb;pdb.set_trace()
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductsList(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     # filterset_fields  = ['name']


class ProductDetails(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        # import pdb;pdb.set_trace()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsListGeneric(ListCreateAPIView):
    queryset = Product.objects.all()[:10]
    serializer_class = ProductSerializerGeneric


class ProductDetailsGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerGeneric


class VendorsList(ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get(self, request, format=None):
        vendors = Vendor.objects.all()[:10]
        # import pdb;pdb.set_trace()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetails(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vendor = self.get_object(pk)
        # import pdb;pdb.set_trace()
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerDetails(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.select_related('passport').prefetch_related(
        Prefetch('customerreview_set', queryset=CustomerReview.objects.all()[:10], to_attr='reviews')
    ).annotate(customer_avg_rating=Avg('customerreview__rating')).prefetch_related(
        Prefetch('products', queryset=Product.objects.annotate(product_count=Count('id'), total=ExpressionWrapper(
            F('price') * F('product_count'), output_field=FloatField()))))

    serializer_class = CustomerDetailsSerializer


class ProductCustomers(RetrieveAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch('customer_set', queryset=Customer.objects.all(), to_attr='customers'))
    serializer_class = ProductCustomersSerializer


class VendorViewSet(viewsets.ModelViewSet):
    # http://127.0.0.1:8000/api/v1/vendors-view-set/
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # http://127.0.0.1:8000/api/v1/vendors-view-set/?page_size=20
    pagination_class = StandardResultsSetPagination

    # http://127.0.0.1:8000/api/v1/vendors-view-set/?ordering=name?inn=12345678&search=Argent
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'address', 'email', 'phone', 'inn']
    search_fields = ['name', 'address', 'email', 'phone', 'inn']
    ordering_fields = '__all__'

    # for not found
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #
    #     if not page:
    #         return Response({'error': '404', 'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
