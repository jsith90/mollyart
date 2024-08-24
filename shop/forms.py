from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image', 'quantity', 'is_sale', 'sale_price', 'is_sold_out']
        labels = {
            'name': 'Product Name:',
            'price': 'Price:',
            'category':'Category:',
            'description': 'Description:',
            'image': 'Uploade main image:',
            'image2': 'Uploade an additional image:',
            'image3': 'Uploade an additional image:',
            'image4': 'Uploade an additional image:',
            'quantity': 'Quantity:',
            'is_sale': 'Tick box for Sale:',
            'sale_price': 'Sale Price:',
            'is_sold_out': 'Tick box for Sold Out',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your product description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_sold_out': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'New Category Name:',
            }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name...'})
            }
