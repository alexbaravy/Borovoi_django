from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from ecoshop.models import Customer, CustomerReview, Passport, Product, ProductReview, Vendor, VendorReview, Category
from django.utils.safestring import mark_safe

''' Start Block Inline '''


class BaseInLine(admin.TabularInline):
    extra = 1


class ProductInLine(BaseInLine):
    model = Product


class PassportInLine(BaseInLine):
    model = Passport


class VendorReviewInLine(BaseInLine):
    model = VendorReview


class ProductReviewInLine(BaseInLine):
    model = ProductReview


class CustomerReviewInLine(BaseInLine):
    model = CustomerReview


''' End Block Inline '''


@admin.display(description='photo')
def get_html_photo(objects):
    if objects.photo:
        return mark_safe(f'<img src={objects.photo.url} width=50>')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', get_html_photo]

    # inlines = [ProductInLine]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(product_count=Count('product'))
        return queryset

    def product_count(self, obj):
        return obj.product_count

    product_count.short_description = 'count products'
    product_count.admin_order_field = 'product_count'


class CountReviewMixin():
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(count_review=Count(self.count_field))
        return queryset

    def count_review(self, obj):
        return obj.count_review

    count_review.short_description = 'Reviews'
    count_review.admin_order_field = 'count_review'


@admin.register(Customer)
class CustomerAdmin(CountReviewMixin, admin.ModelAdmin):
    list_display = ['name', 'address', 'email', 'phone', 'count_review', get_html_photo]
    search_fields = ['name', 'address', 'email', 'phone']
    count_field = 'customerreview'
    # filter_horizontal = ('products',)
    raw_id_fields = ('products',)
    inlines = [PassportInLine, CustomerReviewInLine]


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ['customer', 'passport_series', 'passport_number']
    list_filter = ['passport_series']


@admin.register(Product)
class ProductAdmin(CountReviewMixin, admin.ModelAdmin):
    actions = ['mark_amount']

    def mark_amount(modeladmin, request, queryset):
        for product in queryset:
            if product.amount == 0 and '-[deleted]' not in product.name:
                product.name = f'{product.name}-[deleted]'
            elif product.amount > 0 and '-[deleted]' in product.name:
                product.name = product.name.replace("-[deleted]", "")
            product.save()

    mark_amount.short_description = "Mark as zero amount"

    list_display = ['name', 'price', 'amount', 'date', 'count_review', get_html_photo]
    search_fields = ['name', 'price', 'amount', 'date']
    list_filter = ('category',)
    count_field = 'productreview'
    inlines = [ProductReviewInLine]


@admin.register(Vendor)
class VendorAdmin(CountReviewMixin, admin.ModelAdmin):
    list_display = ['name', 'address', 'email', 'phone', 'count_review', get_html_photo]
    search_fields = ['name', 'address', 'email', 'phone']
    count_field = 'vendorreview'
    # filter_horizontal = ('products',)
    raw_id_fields = ('products',)

    inlines = [VendorReviewInLine]


''' Start Block Reviews'''


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'title', 'rating', 'author', 'date']
    search_fields = ['customer', 'rating', 'author']
    list_per_page = 30
    ordering = ('-date',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'rating', 'author', 'date']
    search_fields = ['product', 'rating', 'author']
    list_per_page = 30
    ordering = ('-date',)


@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'title', 'rating', 'author', 'date']
    search_fields = ['vendor', 'rating', 'author']
    list_per_page = 30
    ordering = ('-date',)


'''End Block Reviews'''
