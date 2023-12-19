from django.test import TestCase
from ecoshop.forms import ProductForm
from ecoshop.models import Category, Product

# 7)	Протестируйте форму и одну из views  на предмет получения корректных данных.
class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_valid_form(self):
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 10.0,
            'amount': 5,
            'photo': 'image_not_found.jpg',
            'category': self.category.id,
        }
        form = ProductForm(data)

        if not form.is_valid():
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {}
        form = ProductForm(data)
        self.assertFalse(form.is_valid())
