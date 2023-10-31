from .models import Customer, Vendor, Product, ProductReview
import factory
from faker import Faker

fake = Faker()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda _: f"{fake.first_name()} {fake.last_name()}")
    address = factory.LazyAttribute(lambda _: fake.address())
    email = factory.LazyAttribute(lambda _: fake.email())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:16])
    discount = fake.random_element(elements=[0, 5, 10])


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor

    name = factory.LazyAttribute(lambda _: fake.company())
    address = factory.LazyAttribute(lambda _: fake.address())
    email = factory.LazyAttribute(lambda _: fake.email())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:16])
    inn = fake.random_int(min=1000000000, max=9999999999)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: f"{fake.word()} {fake.word()} {fake.word()}")
    description = factory.LazyFunction(lambda: fake.sentence())
    price = fake.random_int(min=1, max=100)
    amount = fake.random_int(min=100, max=999)
    category = fake.random_int(min=1, max=17)


class ProductReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductReview

    title = factory.LazyAttribute(lambda _: f"{fake.word()} {fake.word()} {fake.word()}")
    description = factory.LazyFunction(lambda: fake.sentence())
    rating = fake.random_int(min=1, max=10)
    product = factory.Iterator(Product.objects.all())
    author = factory.Iterator(Customer.objects.all())
