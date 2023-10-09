from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import json
import os


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
    json_data = load_json_data('products_categories.json','sale.json')
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
