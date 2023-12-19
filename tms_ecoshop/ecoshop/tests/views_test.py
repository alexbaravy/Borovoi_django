from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ecoshop.models import Category, Product
from base64 import b64encode
from unittest.mock import patch, MagicMock
import time

#7)	Протестируйте форму и одну из views  на предмет получения корректных данных.
class AddProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='ecoshop', password='ecoshop')
        self.category = Category.objects.create(name='Test Category')

    def test_add_product_view_get(self):
        self.client.login(username='ecoshop', password='ecoshop')
        response = self.client.get(reverse('ecoshop:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_add_product.html')

    def test_add_product_view_get_invalid(self):
        response = self.client.get(reverse('ecoshop:add_product'))
        self.assertEqual(response.status_code, 302)
#8)	*В одну из вьюшек добавьте “искусственную нагрузку”  с помощью модуля time и функции sleep на 30 секунд. Протестируйте данную вьюшку используя Mock и декоратор @patch
    @patch('ecoshop.views.time.sleep', return_value=None)
    @patch('ecoshop.tasks.requests')
    def test_add_product_view_post(self, fake_requests, mock_sleep):
        img_content = b'12345678'
        fake_response = MagicMock()
        fake_requests.post.return_value = fake_response
        fake_response.json.return_value = {'images': [b64encode(img_content)]}

        self.client.login(username='ecoshop', password='ecoshop')

        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '123',
            'amount': '123',
            'photo': 'image_not_found.jpg',
            'category': self.category.id,
        }

        response = self.client.post(reverse('ecoshop:add_product'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertRedirects(response, reverse('ecoshop:add_product'))
        self.assertContains(response, 'Product added successfully')
        mock_sleep.assert_called_once_with(30)