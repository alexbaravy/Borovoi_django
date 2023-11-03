from django.urls import path



from . import views

app_name = 'ecoshop'

urlpatterns = [
    # http://127.0.0.1:8000/ecoshop/
    path("", views.index, name="index"),
    # http://127.0.0.1:8000/ecoshop/shop-grid/
    path("shop-grid/", views.shop_grid, name="shop_grid"),
    # http://127.0.0.1:8000/ecoshop/shop-grid/shop-details/
    path("shop-grid/shop-details/", views.shop_details, name="shop_details"),
    path("shop-grid/<str:category>/", views.shop_grid, name="shop_grid"),
    # path("shop-grid/<str:category>/<int:id>/", views.shop_details, name="shop_grid"),
    # http://127.0.0.1:8000/ecoshop/shoping-cart/
    path("shoping-cart/", views.shoping_cart, name="shoping_cart"),
    # http://127.0.0.1:8000/ecoshop/checkout/
    path("checkout/", views.checkout, name="checkout"),
    # http://127.0.0.1:8000/ecoshop/blog/
    path("blog/", views.blog, name="blog"),
    # http://127.0.0.1:8000/ecoshop/blog/blog-details/
    path("blog/blog-details/", views.blog_details, name="blog_details"),
    # http://127.0.0.1:8000/ecoshop/contact/
    path("contact/", views.contact, name="contact"),
    # http://127.0.0.1:8000/ecoshop/tasks-3/
    path("tasks-3/", views.tasks_3, name="tasks_3"),
    # http://127.0.0.1:8000/ecoshop/tasks-4/
    path("tasks-4/", views.tasks_4, name="tasks_4"),
    # http://127.0.0.1:8000/ecoshop/vendors/
    path("vendors/", views.vendors, name="vendors"),
    # http://127.0.0.1:8000/ecoshop/vendors/vendor_id/
    path("vendors/<int:vendor_id>/", views.vendor_detail, name="vendor_detail"),
    # http://127.0.0.1:8000/ecoshop/customers/
    path("customers/", views.customers, name="customers"),
    # http://127.0.0.1:8000/ecoshop/customers/customer_id/
    path("customers/<int:customer_id>/", views.customer_detail, name="customer_detail"),
    # http://127.0.0.1:8000/ecoshop/tasks-6/
    path("tasks-6/", views.tasks_6, name="tasks_6"),
]
