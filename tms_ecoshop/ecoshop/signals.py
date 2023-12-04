from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


# @receiver(pre_save, sender=Product)
# def mark_amount(sender, instance, **kwargs):
#     if instance.amount == 0 and '-[deleted]' not in instance.name:
#         instance.name = f'{instance.name}-[deleted]'
#     elif instance.amount > 0 and '-[deleted]' in instance.name:
#         instance.name = instance.name.replace("-[deleted]", "")

