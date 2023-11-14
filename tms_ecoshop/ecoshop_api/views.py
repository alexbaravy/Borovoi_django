from django.shortcuts import render, HttpResponse
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, viewsets
from django.http import Http404
from ecoshop.models import Customer, CustomerReview, Product, Vendor
from ecoshop_api.serializers import CustomerDetailsSerializer, ProductCustomersSerializer, ProductSerializer, \
    ProductSerializerGeneric, \
    VendorSerializer
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, Max, ExpressionWrapper, FloatField, Avg, Subquery, F, Sum, Prefetch


class ProductsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        products = Product.objects.all()[:10]
        # import pdb;pdb.set_trace()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
