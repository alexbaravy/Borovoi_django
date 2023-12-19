from django.test import TestCase
from django.utils import timezone
from ecoshop.models import Product, Category
from django.core.exceptions import ValidationError

#6)	Протестируйте одну из ваших Django моделей, используя models_test.py.
class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            photo='image_not_found.jpg',
            price=50.99,
            amount=10,
            date=timezone.now(),
            category=self.category
        )

    def test_create_product(self):
        self.assertEqual(self.product.photo, 'image_not_found.jpg')
        self.assertEqual(self.product.price, 50.99)
        self.assertEqual(self.product.amount, 10)
        self.assertEqual(self.product.date.date(), timezone.now().date())
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(Product.objects.count(), 1)

    def test_price_validator(self):
        with self.assertRaises(ValidationError):
            self.product.price = 1000000000
            self.product.full_clean()
