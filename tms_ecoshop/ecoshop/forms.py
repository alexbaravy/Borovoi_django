from django import forms
from .models import Category, CustomerReview, Product, ProductReview, VendorReview
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'amount', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
            'price': forms.TextInput(attrs={'placeholder': 'Enter price'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Enter amount'}),
            'category': forms.Select(attrs={'placeholder': 'Select product category'}),
        }


class ProductFormCrispy(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date']

        widgets = {
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 3})
        }


class BaseReviewForm(forms.ModelForm):
    class Meta:
        model = None
        fields = ['title', 'description', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
            'rating': forms.Select(attrs={'placeholder': 'Enter price'}),

        }


class CustomerReviewForm(BaseReviewForm):
    class Meta(BaseReviewForm.Meta):
        model = CustomerReview


class ProductReviewForm(BaseReviewForm):
    class Meta(BaseReviewForm.Meta):
        model = ProductReview


class VendorReviewForm(BaseReviewForm):
    class Meta(BaseReviewForm.Meta):
        model = VendorReview
