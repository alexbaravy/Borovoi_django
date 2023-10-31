from django.contrib import admin
from ecoshop.models import Category, Customer, Passport, Product, ProductReview, Vendor


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'amount', 'category']

    @admin.display(description='name')
    def view_name(self, obj):
        return obj.name[:10]


# admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(Passport)

admin.site.register(ProductReview)
# admin.site.register(VendorRating)
# admin.site.register(CustomerRating)
