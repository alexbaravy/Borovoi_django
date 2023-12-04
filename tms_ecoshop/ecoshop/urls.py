from django.urls import path
from . import views
# from .views import FeedbackFormView, SuccessView
from django.contrib.auth.views import LoginView


app_name = 'ecoshop'

urlpatterns = [
    # http://127.0.0.1:8000/ecoshop/
    path("", views.index, name="index"),
    # http://127.0.0.1:8000/ecoshop/shop-grid/
    path("products/", views.products, name="products"),
    # http://127.0.0.1:8000/ecoshop/shop-grid/product-details/
    # path("shop-grid/product-details/", views.product_details, name="product_details"),
    path("products/<str:category>/", views.products, name="products"),
    path("products/<str:category_url>/<int:id>/", views.product_details, name="product_details"),
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
    path("vendors/<int:vendor_id>/", views.vendor_details, name="vendor_details"),
    # http://127.0.0.1:8000/ecoshop/customers/
    path("customers/", views.customers, name="customers"),
    # http://127.0.0.1:8000/ecoshop/customers/customer_id/
    path("customers/<int:customer_id>/", views.customer_details, name="customer_details"),
    # http://127.0.0.1:8000/ecoshop/tasks-6/
    path("tasks-6/", views.tasks_6, name="tasks_6"),
    # http://127.0.0.1:8000/ecoshop/add-product/
    path("add-product/", views.add_product, name="add_product"),
    # http://127.0.0.1:8000/ecoshop/add-product/
    path("sign-up/", views.sign_up, name="sign_up"),
    path('accounts/login/', LoginView.as_view(), name='login'),

    # path("feedback", FeedbackFormView.as_view(), name="feedback"),
    # path("feedback/success/", SuccessView.as_view(), name="success"),

]
