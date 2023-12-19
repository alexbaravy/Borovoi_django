from django.db.models.functions import Round
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import json
import os
from ecoshop.models import Category, Customer, CustomerReview, Passport, Product, ProductReview, Vendor, VendorReview
from datetime import date, datetime
import random
from django.db.models import Count, Max, ExpressionWrapper, FloatField, Avg, Subquery, F, Sum, Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import CustomerReviewForm, ProductForm, ProductReviewForm, VendorReviewForm, ProductFormCrispy, SignUpForm
from django.views.generic import UpdateView

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .tasks import generate_photo
from django.contrib.auth.decorators import login_required, permission_required
import time


def breadcrumb(title):
    breadcrumb = [{'title': 'Home', 'url': reverse('ecoshop:index')}]

    # for delete
    if title == 'Tasks 6. Django':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:tasks_6')})

    return {'breadcrumb': breadcrumb}


def get_paginator(request, queryset, items_per_page=16):
    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


''' Forms Begin '''


def handle_review_form(request, context, detail_object, author, model):
    author_ids = list(author.objects.values_list('id', flat=True))
    random_author = author.objects.get(id=random.choice(author_ids))
    context.update({'random_author': random_author})

    if request.method == 'POST':
        review_form = model(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.customer = detail_object if hasattr(detail_object, 'id') else None
            review.product = detail_object if hasattr(detail_object, 'id') else None
            review.vendor = detail_object if hasattr(detail_object, 'id') else None
            review.author = random_author
            review.save()
            messages.success(request, 'Review added successfully')

            if hasattr(detail_object, 'id'):
                if isinstance(detail_object, Vendor):
                    cache_key = 'vendors_page'
                    cache.delete(cache_key)

            return redirect(request.get_full_path())
        else:
            messages.success(request, 'WTF?')
    else:
        review_form = model

    return review_form


@login_required()
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            amount = request.POST['amount']
            category = Category.objects.get(pk=request.POST['category'])

            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                product = Product(name=name,
                                  description=description,
                                  photo=photo,
                                  price=price,
                                  amount=amount,
                                  category=category)

                product.save()
            else:
                # generate_photo.delay(name=name, description=description, price=price, amount=amount,
                #                      category_id=category.id)

                # without celery
                generate_photo(name=name, description=description, price=price, amount=amount,
                                     category_id=category.id)

            time.sleep(30)
            messages.success(request, 'Product added successfully')
            cache_keys = ['categories_page', 'vendors_page', 'products_page_all',
                          f'products_page_{request.POST["category"]}']
            cache.delete_many(cache_keys)
            return redirect('ecoshop:add_product')
        else:
            messages.success(request, 'WTF?')
    else:
        form = ProductForm()

    return render(request, 'form_add_product.html', {'form': form})


''' Forms End '''


def load_json_data(*json_files):
    current_path = os.path.dirname((os.path.abspath(__file__)))
    json_data = {}

    for filename in json_files:
        json_path = os.path.join(current_path, filename)
        with open(json_path, 'r') as file:
            json_data[os.path.splitext(filename)[0]] = json.load(file)
    return json_data


# categories menu with count products
def hero(request):
    cache_key = 'categories_page'
    categories = cache.get(cache_key)
    if categories is None:
        categories = Category.objects.annotate(product_count=Count('product'))
        cache.set(cache_key, categories, 60 * 30)
    return {'products_categories': list(categories.values())}


@cache_page(60 * 10, cache='redis')
def index(request):
    context = breadcrumb("Main")
    json_data = load_json_data('products_latest.json', 'products_featured.json')
    context.update(json_data)
    context.update(hero(request))

    return render(request, "index.html", context)


def blog(request):
    add.delay(19, 6)
    context = breadcrumb("Blog")
    context['breadcrumb'].append({'title': 'Blog', 'url': reverse('ecoshop:blog')})
    context.update(hero(request))
    return render(request, "blog.html", context)


def blog_details(request):
    context = breadcrumb("Blog Details")
    context.update(hero(request))
    return render(request, "blog_details.html", context)


def checkout(request):
    context = breadcrumb("Checkout")
    context['breadcrumb'].append({'title': 'Checkout', 'url': reverse('ecoshop:checkout')})
    context.update(hero(request))
    return render(request, "checkout.html", context)


def contact(request):
    context = breadcrumb("Contact")
    context['breadcrumb'].append({'title': 'Contact', 'url': reverse('ecoshop:shoping_cart')})
    context.update(hero(request))
    return render(request, "contact.html", context)


def shoping_cart(request):
    context = breadcrumb("Shoping Cart")
    context['breadcrumb'].append({'title': 'Shoping Cart', 'url': reverse('ecoshop:shoping_cart')})
    context.update(hero(request))
    return render(request, "shoping_cart.html", context)


''' Customers Begin '''


@permission_required('is_superuser', raise_exception=True)
@cache_page(60 * 10, cache='redis')
def customers(request):
    context = breadcrumb("Customers")

    customers = Customer.objects.all()

    page_obj = get_paginator(request, customers, items_per_page=16)

    context.update({'items': page_obj})

    context['breadcrumb'].append(
        {'title': f"Customers: {len(customers)} found", 'url': reverse('ecoshop:customers')})
    context.update(hero(request))

    return render(request, 'customers.html', context)


@permission_required('is_superuser', raise_exception=True)
@cache_page(60 * 20, cache='static_html')
def customer_details(request, customer_id):
    customer_details = Customer.objects.select_related('passport').prefetch_related(
        'customerreview_set').annotate(customer_avg_rating=Avg('customerreview__rating')).prefetch_related(
        Prefetch('products', queryset=Product.objects.annotate(product_count=Count('id'), total=ExpressionWrapper(
            F('price') * F('product_count'), output_field=FloatField())))).get(pk=customer_id)

    if customer_details.customer_avg_rating is not None:
        customer_details.customer_avg_rating = round(customer_details.customer_avg_rating, 2)

    context = breadcrumb(customer_details.name)
    context['breadcrumb'].extend(
        [{'title': 'Customers', 'url': reverse('ecoshop:customers')},
         {'title': customer_details.name, 'url': reverse('ecoshop:customer_details', args=[customer_id])}])
    context.update(hero(request))

    context.update({'customer_details': customer_details})

    total_amount = customer_details.products.aggregate(total_amount=Sum('total'))['total_amount']

    context.update({'total_amount': total_amount})

    review_form = handle_review_form(request, context, customer_details, Vendor, CustomerReviewForm)
    context.update({'review_form': review_form})

    return render(request, 'customer_details.html', context)


''' Customers End '''

''' Products Begin '''


def products(request, category=None):
    context = breadcrumb("Shop")
    context['breadcrumb'].append({'title': "Shop", 'url': reverse('ecoshop:products')})
    hero_menu = hero(request)

    category_data = None
    for data in hero_menu['products_categories']:
        if data['url'] == category:
            category_data = data
            break

    context.update(hero_menu)

    context['current_category'] = category_data
    if context['current_category']:
        context['breadcrumb'].append(
            {'title': context['current_category']['name'], 'url': context['current_category']['url']})
        cache_key = f"products_page_{context['current_category']['id']}"
        products = cache.get(cache_key)
    else:
        cache_key = f"products_page_all"
        products = cache.get(cache_key)

    if products is None:
        if category is None:
            products = Product.objects.all().order_by('id')
        else:
            products = Product.objects.filter(category=category_data['id'])
        cache.set(cache_key, products, 60 * 30)
    page_obj = get_paginator(request, products, items_per_page=64)
    context.update({'items': page_obj})

    return render(request, "products.html", context)


# @cache_page(60 * 20, cache='static_html')
def product_details(request, category_url, id):
    context = breadcrumb("Shop Details")

    product_details = Product.objects.annotate(count_reviews=Count('productreview')).prefetch_related(
        'productreview_set').get(pk=id)
    context.update({'product_details': product_details})

    context['breadcrumb'].extend([
        {'title': 'Shop', 'url': reverse('ecoshop:products')},
        {'title': product_details.category, 'url': reverse('ecoshop:products', args=[product_details.category.url])},
        {'title': product_details.name, 'url': reverse('ecoshop:products')}
    ])

    context.update(hero(request))

    review_form = handle_review_form(request, context, product_details, Customer, ProductReviewForm)
    context.update({'review_form': review_form})

    return render(request, "product_details.html", context)


''' Products End '''

''' Vendors Begin '''


@permission_required('is_superuser', raise_exception=True)
def vendors(request):
    context = breadcrumb("Vendors")
    cache_key = 'vendors_page'
    vendors = cache.get(cache_key)
    if vendors is None:
        vendors = Vendor.objects.annotate(product_count=Count('products', distinct=True),
                                          review_count=Count('vendorreview', distinct=True)).values('id', 'name',
                                                                                                    'photo',
                                                                                                    'product_count',
                                                                                                    'review_count')
        cache.set(cache_key, vendors, 60 * 30)
    page_obj = get_paginator(request, vendors, items_per_page=16)
    context.update({'items': page_obj})

    context['breadcrumb'].append(
        {'title': f"Vendors: {len(vendors)} found", 'url': reverse('ecoshop:vendors')})
    context.update(hero(request))

    return render(request, 'vendors.html', context)


@permission_required('is_superuser', raise_exception=True)
@cache_page(60 * 20, cache='static_html')
def vendor_details(request, vendor_id):
    context = breadcrumb("Vendor Detail")

    vendor_details = Vendor.objects.annotate(vendor_avg_rating=Avg('vendorreview__rating')).prefetch_related(
        'vendorreview_set').prefetch_related(
        Prefetch('products', queryset=Product.objects.annotate(product_reviews=Count('productreview')))).get(
        pk=vendor_id)

    context['breadcrumb'].extend([
        {'title': "Vendors", 'url': reverse('ecoshop:vendors')},
        {'title': vendor_details.name, 'url': reverse('ecoshop:vendor_details', args=[vendor_id])}
    ])
    context.update(hero(request))

    vendor_details.vendor_avg_rating = round(vendor_details.vendor_avg_rating, 2)

    context.update({'vendor_details': vendor_details})

    review_form = handle_review_form(request, context, vendor_details, Customer, VendorReviewForm)
    context.update({'review_form': review_form})

    return render(request, 'vendor_details.html', context)


''' Vendors End '''


def sign_up(request):
    context = breadcrumb("Sign up")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ecoshop:sign_up')
        else:
            messages.success(request, 'WTF?')
    else:
        form = SignUpForm()

    return render(request, 'form_sign_up.html', {'form': form})


''' Tasks Begin '''


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

    product_with_other_vendors = Product.objects.annotate(vendor_count=Count('vendors')).values('name',
                                                                                                'vendor_count').filter(
        vendor_count__gt=1)
    context.update({'product_with_other_vendors': list(product_with_other_vendors)})

    return render(request, 'tasks_4.html', context)


def tasks_6(request):
    context = breadcrumb("Tasks 6. Django")

    # 2) Получить     среднюю    цену    продукта.:
    avg_price = Product.objects.aggregate(avg_price=Avg('price'))['avg_price']
    avg_price = round(avg_price, 2)
    context.update({'avg_price': avg_price})

    # 3)	Получить суммарное количество продуктов каждой категории:
    product_count_categories = Category.objects.annotate(product_count=Count('product'))
    context.update({'product_count_categories': product_count_categories})

    # 4)    Получить     количество    отзывов    для    каждого    продукта
    review_count_product = Product.objects.annotate(review_count=Count('productreview')).order_by('-review_count')
    context.update({'review_count_product': review_count_product})

    # 5)	Получить общее количество продуктов, у которых цена больше 50.
    price_over_50 = Product.objects.filter(price__gt=50).count()
    context.update({'price_over_50': price_over_50})

    # 6)	Получить максимальную цену для каждой категории продуктов.
    max_price_category = Category.objects.annotate(max_price=Max('product__price'))
    context.update({'max_price_category': max_price_category})

    # 7)	Получить суммарное количество продуктов и среднюю цену для каждого поставщика.
    count_avg_vendor = Vendor.objects.annotate(product_sum=Sum('products__amount'),
                                               avg_price=Round(Avg('products__price'), 2))
    context.update({'count_avg_vendor': count_avg_vendor})

    # 8)    Получить     общее    количество    продуктов    и    среднее    количество    отзывов    для    каждого    поставщика.
    # сумму отзывов делим на количество разных товаров

    avg_review_product_vendor = Vendor.objects.annotate(
        count_products=Count('products__id', distinct=True),
        count_reviews=Count('vendorreview__id', distinct=True),
        avg_reviews=ExpressionWrapper(
            Count('vendorreview__id', distinct=True) / Count('products__id', distinct=True),
            output_field=FloatField()
        )
    ).values('id', 'name', 'count_products', 'count_reviews', 'avg_reviews')

    avg_review_product_vendor = avg_review_product_vendor.filter(
        count_products__gt=0)

    context.update({'avg_review_product_vendor': avg_review_product_vendor})

    # 9) *Получить среднее количество продуктов для каждой категории, а также суммарное количество отзывов для продуктов каждой категории.
    # Нету среднего количества продуктов в категории, есть общее количество продуктов, так и считаю

    count_product_rating_category = Product.objects.values('category__name').annotate(count_products=Count('id'),
                                                                                      count_reviews=Count(
                                                                                          'productreview'))
    context.update({'count_product_rating_category': count_product_rating_category})

    # 10)    *Получить     общее    количество    продуктов    для    каждого    поставщика    и    среднее    количество    отзывов    для    продуктов    каждого    поставщика.
    # тоже самое, отзывы делим на количество наименований?

    avg_review_product_vendor2 = Product.objects.values('vendor__name').annotate(
        count_products=Count('id', distinct=True),
        count_reviews=Count('productreview__id', distinct=True),
        avg_reviews=ExpressionWrapper(
            Count('productreview__id', distinct=True) / Count('id', distinct=True),
            output_field=FloatField()
        )
    )

    avg_review_product_vendor2 = avg_review_product_vendor2.filter(
        count_products__gt=0)

    context.update({'avg_review_product_vendor2': avg_review_product_vendor2})

    return render(request, 'tasks_6.html', context)


''' Tasks End '''
