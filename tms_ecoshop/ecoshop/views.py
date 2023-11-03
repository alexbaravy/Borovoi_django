from django.db.models.functions import Round
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
import json
import os
from ecoshop.models import Category, Customer, Passport, Product, Vendor, ProductReview
from datetime import date, datetime
import random
from django.db.models import Count, Max, ExpressionWrapper, FloatField, Avg, Subquery, F, Sum, Prefetch


def breadcrumb(title):
    breadcrumb = [{'title': 'Home', 'url': reverse('ecoshop:index')}]

    # for delete
    if title == 'Tasks 6. Django':
        breadcrumb.append({'title': title, 'url': reverse('ecoshop:tasks_6')})

    return {'breadcrumb': breadcrumb}


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
    categories = Category.objects.annotate(product_count=Count('product'))
    return {'products_categories': list(categories.values())}


def index(request):
    context = breadcrumb("Main")
    json_data = load_json_data('products_latest.json', 'products_featured.json')
    context.update(json_data)
    context.update(hero(request))

    return render(request, "index.html", context)


def shop_grid(request, category=None):
    print(category)
    context = breadcrumb("Shop")
    context['breadcrumb'].append({'title': "Shop", 'url': reverse('ecoshop:shop_grid')})

    json_data = load_json_data('saleoff.json', 'sale.json', 'products_latest.json')
    hero_menu = hero(request)

    category_data = None
    for data in hero_menu['products_categories']:
        if data['url'] == category:
            category_data = data
            break

    context.update(json_data)
    context.update(hero_menu)

    context['current_category'] = category_data
    if context['current_category']:
        context['breadcrumb'].append(
            {'title': context['current_category']['name'], 'url': context['current_category']['url']})

    if category is None:
        products = Product.objects.all()[:16]
    else:
        products = Product.objects.filter(category=category_data['id'])[:16]

    context.update({'products': list(products)})

    return render(request, "shop_grid.html", context)


def shop_details(request):
    context = breadcrumb("Shop Details")
    context['breadcrumb'].extend([
        {'title': 'Shop', 'url': reverse('ecoshop:shop_grid')},
        {'title': 'Shop Detail', 'url': reverse('ecoshop:shop_details')}
    ])

    json_data = load_json_data('sale.json')
    context.update(json_data)
    context.update(hero(request))
    return render(request, "shop_details.html", context)


def shoping_cart(request):
    context = breadcrumb("Shoping Cart")
    context['breadcrumb'].append({'title': 'Shoping Cart', 'url': reverse('ecoshop:shoping_cart')})
    context.update(hero(request))
    return render(request, "shoping_cart.html", context)


def checkout(request):
    context = breadcrumb("Checkout")
    context['breadcrumb'].append({'title': 'Checkout', 'url': reverse('ecoshop:checkout')})
    context.update(hero(request))
    return render(request, "checkout.html", context)


def blog(request):
    context = breadcrumb("Blog")
    context['breadcrumb'].append({'title': 'Blog', 'url': reverse('ecoshop:blog')})
    context.update(hero(request))
    return render(request, "blog.html", context)


def blog_details(request):
    context = breadcrumb("Blog Details")
    context.update(hero(request))
    return render(request, "blog_details.html", context)


def contact(request):
    context = breadcrumb("Contact")
    context['breadcrumb'].append({'title': 'Contact', 'url': reverse('ecoshop:shoping_cart')})
    context.update(hero(request))
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

    product_with_other_vendors = Product.objects.annotate(vendor_count=Count('vendors')).values('name',
                                                                                                'vendor_count').filter(
        vendor_count__gt=1)
    context.update({'product_with_other_vendors': list(product_with_other_vendors)})

    return render(request, 'tasks_4.html', context)


def vendors(request):
    context = breadcrumb("Vendors")
    context['breadcrumb'].append(
        {'title': "Vendors", 'url': reverse('ecoshop:vendors')})
    context.update(hero(request))

    vendors = Vendor.objects.annotate(product_count=Count('products', distinct=True),
                                      review_count=Count('vendorreview', distinct=True)).values('id', 'name',
                                                                                                'product_count',
                                                                                                'review_count')

    context.update({'vendors': list(vendors)})
    context.update({'vendors_count': len(vendors)})

    return render(request, 'vendors.html', context)


def vendor_detail(request, vendor_id):
    context = breadcrumb("Vendor Detail")

    vendor_detail = Vendor.objects.annotate(vendor_avg_rating=Avg('vendorreview__rating')).prefetch_related(
        'vendorreview_set').prefetch_related(
        Prefetch('products', queryset=Product.objects.annotate(product_reviews=Count('productreview')))).get(
        pk=vendor_id)

    context['breadcrumb'].extend([
        {'title': "Vendors", 'url': reverse('ecoshop:vendors')},
        {'title': vendor_detail.name, 'url': reverse('ecoshop:vendor_detail', args=[vendor_id])}
    ])

    context.update(hero(request))

    vendor_detail.vendor_avg_rating = round(vendor_detail.vendor_avg_rating, 2)

    context.update({'vendor_detail': vendor_detail})

    return render(request, 'vendor_detail.html', context)


def customers(request):
    context = breadcrumb("Customers")
    context['breadcrumb'].append(
        {'title': "Customers", 'url': reverse('ecoshop:customers')})

    context.update(hero(request))

    customers = Customer.objects.all()
    context.update({'customers': list(customers)})
    context.update({'customers_count': len(customers)})

    return render(request, 'customers.html', context)


def customer_detail(request, customer_id):
    customer_detail = Customer.objects.select_related('passport').prefetch_related(
        'customerreview_set').annotate(customer_avg_rating=Avg('customerreview__rating')).prefetch_related(
        Prefetch('products', queryset=Product.objects.annotate(product_count=Count('id'), total=ExpressionWrapper(
            F('price') * F('product_count'), output_field=FloatField())))).get(pk=customer_id)

    if customer_detail.customer_avg_rating is not None:
        customer_detail.customer_avg_rating = round(customer_detail.customer_avg_rating, 2)

    context = breadcrumb(customer_detail.name)
    context['breadcrumb'].extend(
        [{'title': 'Customers', 'url': reverse('ecoshop:customers')},
         {'title': customer_detail.name, 'url': reverse('ecoshop:customer_detail', args=[customer_id])}])

    context.update(hero(request))

    # customer_detail = Customer.objects.select_related('passport').prefetch_related(
    #     'customerreview_set').annotate(customer_avg_rating=Avg('customerreview__rating')).get(pk=customer_id)

    context.update({'customer_detail': customer_detail})

    # customer_purchases = Product.objects.annotate(product_count=Count('id')).filter(customers__id=customer_id)
    # customer_purchases = Product.objects.annotate(product_count=Count('id')).filter(customers__id=customer_id).annotate(
    #     total=ExpressionWrapper(F('price') * F('product_count'), output_field=FloatField())
    # ).values('id', 'name', 'price', 'product_count', 'total')

    # context.update({'customer_purchases': customer_purchases})

    total_amount = customer_detail.products.aggregate(total_amount=Sum('total'))['total_amount']

    context.update({'total_amount': total_amount})

    return render(request, 'customer_detail.html', context)


# def customer_detail(request, customer_id):
#     context = breadcrumb("Customer Detail")
#     context.update({'customer_id': customer_id})
#
#     # customer_detail = Customer.objects.select_related('passport')
#
#     customer_detail = Passport.objects.all()
#
#     for customer in customer_detail:
#         print(customer.customer)
#
#     print(customer_detail)
#
#     return render(request, 'customer_detail.html', context)

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
