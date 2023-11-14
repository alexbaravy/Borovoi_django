from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from ecoshop.models import Customer, Passport, Product, CustomerReview, Vendor


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class ProductSerializerGeneric(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class VendorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(max_length=16)
    inn = serializers.CharField(max_length=12, allow_null=True)

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.inn = validated_data.get('inn', instance.inn)
        instance.save()
        return instance


class PassportSerializer(ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'


class CustomerReviewSerializer(ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = '__all__'


class CustomerDetailsSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'email', 'phone', 'discount', 'customer_avg_rating', 'passport',
                  'product_count', 'total', 'products', 'reviews']

    products = ProductSerializer(many=True, read_only=True)
    reviews = CustomerReviewSerializer(many=True, read_only=True)
    customer_avg_rating = serializers.FloatField(read_only=True)
    passport = PassportSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()



    def get_product_count(self, instance):
        return instance.products.count()

    def get_total(self, instance):
        return sum(product.price for product in instance.products.all())


class CustomerSimpleSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['products']


class ProductCustomersSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'amount', 'date', 'category', 'customers']

    customers = CustomerSimpleSerializer(many=True, read_only=True)
