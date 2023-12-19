import base64
import json
import requests
from django.core.files.base import ContentFile
from celery import shared_task
from django.conf import settings
from .models import Product, Category
from time import sleep
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail



@shared_task
def add(x, y):
    sleep(10)
    return x + y


@shared_task
def generate_photo(name, description, price, amount, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        response = requests.post(
            'https://bf.dallemini.ai/generate',
            json={'prompt': description}
        )
        response.raise_for_status()
        data = base64.b64decode(response.json()['images'][0])
        photo = ContentFile(data, name='hello.png')
        Product.objects.create(name=name, description=description, photo=photo, price=price, amount=amount,
                               category=category)

        return f"{Product}"
    except requests.RequestException as e:
        return f"Request failed: {e}"
    except json.JSONDecodeError as e:
        return f"JSON decoding failed: {e}"
    except KeyError as e:
        return f"KeyError: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# @shared_task()
# def send_feedback_email_task(email_address, message):
#     """Sends an email when the feedback form has been submitted."""
#     sleep(20)  # Simulate expensive operation that freezes Django
#     send_mail(
#         "Your Feedback",
#         f"\t{message}\n\nThank you!",
#         "support@example.com",
#         [email_address],
#         fail_silently=False,
#     )