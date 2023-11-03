from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from ecoshop.models import Customer, CustomerReview, Passport, Product, ProductReview, Vendor, VendorReview, Category

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'amount', 'category']
#
#     @admin.display(description='name')
#     def view_name(self, obj):
#         return obj.name[:10]


''' Start Block Inline '''


class ProductInLine(admin.TabularInline):
    model = Product
    extra = 1


class PassportInLine(admin.TabularInline):
    model = Passport
    extra = 1


class VendorReviewInLine(admin.TabularInline):
    model = VendorReview
    extra = 1


class ProductReviewInLine(admin.TabularInline):
    model = ProductReview
    extra = 1


class CustomerReviewInLine(admin.TabularInline):
    model = CustomerReview
    extra = 1


''' End Block Inline '''


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count']

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
    list_display = ['name', 'address', 'email', 'phone', 'count_review']
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

    list_display = ['name', 'price', 'amount', 'date', 'count_review']
    search_fields = ['name', 'price', 'amount', 'date']
    list_filter = ('category',)
    count_field = 'productreview'
    inlines = [ProductReviewInLine]


@admin.register(Vendor)
class VendorAdmin(CountReviewMixin, admin.ModelAdmin):
    list_display = ['name', 'address', 'email', 'phone', 'count_review']
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
