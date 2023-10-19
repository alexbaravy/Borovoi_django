from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import json
import os
from ecoshop.models import *
from datetime import date, datetime
import random
from django.db.models import Count, Max, ExpressionWrapper, FloatField, Avg, Subquery


def breadcrumb(title):
    breadcrumb = [{'title': 'Home', 'url': reverse('ecoshop:index')}]

    if title == 'Shop':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:shop_grid')})
    elif title == 'Shop Details':
        breadcrumb.extend([
            {'title': 'Shop', 'url': reverse('ecoshop:shop_grid')},
            {'title': title, 'url': reverse('ecoshop:shop_details')}
        ])
    elif title == 'Shopping Cart':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:shopping_cart')})
    elif title == 'Checkout':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:checkout')})
    elif title == 'Blog':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:blog')})
    elif title == 'Contact':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:contact')})
    elif title == 'Tasks 3. Django':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:tasks_3')})
    elif title == 'Tasks 4. Django':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:tasks_3')})

    return {'breadcrumb': breadcrumb}


def load_json_data(*json_files):
    current_path = os.path.dirname((os.path.abspath(__file__)))
    json_data = {}

    for filename in json_files:
        json_path = os.path.join(current_path, filename)
        with open(json_path, 'r') as file:
            json_data[os.path.splitext(filename)[0]] = json.load(file)
    return json_data


def index(request):
    context = breadcrumb("Main")
    json_data = load_json_data('products_latest.json', 'products_categories.json', 'products_featured.json')
    context.update(json_data)
    return render(request, "index.html", context)


def shop_grid(request, category=None):
    context = breadcrumb("Shop")

    json_data = load_json_data('saleoff.json', 'sale.json', 'products_latest.json', 'products_categories.json')

    category_data = None
    for data in json_data['products_categories']:
        if data['url'] == category:
            category_data = data
            break

    context.update(json_data)

    context['current_category'] = category_data

    if context['current_category']:
        context['breadcrumb'].append(
            {'title': context['current_category']['name'], 'url': context['current_category']['url']})

    return render(request, "shop_grid.html", context)


def shop_details(request):
    context = breadcrumb("Shop Details")
    json_data = load_json_data('products_categories.json', 'sale.json')
    context.update(json_data)
    return render(request, "shop_details.html", context)


def shoping_cart(request):
    context = breadcrumb("Shoping Cart")
    json_data = load_json_data('products_categories.json')
    context.update(json_data)
    return render(request, "shoping_cart.html", context)


def checkout(request):
    context = breadcrumb("Checkout")
    json_data = load_json_data('products_categories.json')
    context.update(json_data)
    return render(request, "checkout.html", context)


def blog(request):
    context = breadcrumb("Blog")
    json_data = load_json_data('products_categories.json')
    context.update(json_data)
    return render(request, "blog.html", context)


def blog_details(request):
    context = breadcrumb("Blog Details")
    json_data = load_json_data('products_categories.json')
    context.update(json_data)
    return render(request, "blog_details.html", context)


def contact(request):
    context = breadcrumb("Contact")
    json_data = load_json_data('products_categories.json')
    context.update(json_data)
    return render(request, "contact.html", context)


def tasks_3(request):
    context = breadcrumb("Tasks 3. Django")

    vendors = Vendor.objects.all()
    context.update({'vendors': list(vendors.values())})

    products_non_meat = Product.objects.exclude(category=5)
    context.update({'products_non_meat': list(products_non_meat.values())})

    search_year_gt = date.today().year - 20
    vendors_gt_20 = Vendor.objects.filter(foundation_year__gt=search_year_gt)
    context.update({'vendors_gt_20': list(vendors_gt_20.values())})

    search_year_lt = date.today().year - 10
    vendors_lt_10 = Vendor.objects.filter(name__startswith="Pana", foundation_year__lt=search_year_lt)
    context.update({'vendors_lt_10': list(vendors_lt_10.values())})

    vendors_young = Vendor.objects.order_by('-foundation_year')[:5]
    context.update({'vendors_young': list(vendors_young.values())})

    products_cost_amount = Product.objects.filter(price__gt=15, amount__lt=150)
    context.update({'products_cost_amount': list(products_cost_amount.values())})

    products_desc_non_def = Product.objects.exclude(description="Perfect Product")
    context.update({'products_desc_non_def': list(products_desc_non_def.values())})

    product_ids = list(Product.objects.values_list('id', flat=True))
    product = Product.objects.get(id=random.choice(product_ids))
    product.delivery_date = datetime.now().strftime('%Y-%m-%d')
    product.save()
    update_date = Product.objects.filter(delivery_date=datetime.now().strftime('%Y-%m-%d'))
    context.update({'update_date': list(update_date.values())})

    return render(request, 'tasks_3.html', context)


def tasks_4(request):
    context = breadcrumb("Tasks 4. Django")

    product = Product.objects.filter(vendors__name='Curtis Family Vineyard')
    context.update({'product': list(product.values())})

    product_gt_with_review = Product.objects.filter(price__gt=30, review__isnull=False).annotate(
        num_reviews=Count('review'))
    context.update({'product_gt_with_review': list(product_gt_with_review.values())})

    product_with_author_review = Product.objects.filter(review__author=11)
    context.update({'product_with_author_review': list(product_with_author_review.values())})

    vendor_with_fruit = Vendor.objects.filter(product__category__name="Health Drinks")
    context.update({'vendor_with_fruit': list(vendor_with_fruit.values())})

    customer_with_passport = Customer.objects.filter(passport__isnull=False)
    context.update({'customer_with_passport': list(customer_with_passport.values())})

    # Отсебятина  (рейтинг то изначально сделал выставляемый) Вывести всех продавцов и покупателей с максимальным средним рейтингом

    # находим максимальный средний рейтинг
    max_avg_rating = VendorRating.objects.values('vendor_id').annotate(
        max_avg_rating=Avg('rating')).order_by('-max_avg_rating')[:1]

    # нахождение вендоров с максимальным рейтингом
    top_vendor = VendorRating.objects.values('vendor__name').annotate(
        max_avg_rating=Avg('rating')
    ).filter(max_avg_rating=max_avg_rating[0]['max_avg_rating'])

    context.update({'top_vendor': list(top_vendor)})

    # находим максимальный средний рейтинг
    max_avg_rating = CustomerRating.objects.values('customer_id').annotate(
        max_avg_rating=Avg('rating')).order_by('-max_avg_rating')[:1]

    # нахождение покупателей с максимальным рейтингом
    top_customer = CustomerRating.objects.values('customer__name').annotate(
        max_avg_rating=Avg('rating')
    ).filter(max_avg_rating=max_avg_rating[0]['max_avg_rating'])

    context.update({'top_customer': list(top_customer)})

    product_without_comments = Product.objects.filter(review__isnull=True)
    context.update({'product_without_comments': list(product_without_comments)})

    customer_with_count_products = Customer.objects.annotate(
        product_count=Count('product')
    ).values('id', 'name', 'product_count').filter(product_count__gt=3).order_by('-product_count')
    context.update({'customer_with_count_products': list(customer_with_count_products)})

    product_with_other_vendors = Product.objects.annotate(vendor_count=Count('vendors')).values('name','vendor_count').filter(vendor_count__gt=1)
    context.update({'product_with_other_vendors': list(product_with_other_vendors)})

    return render(request, 'tasks_4.html', context)
