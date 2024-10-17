from django import forms
from .models import Product, Category, Size
from django.forms import inlineformset_factory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'weight', 'category', 'description', 'image', 'image2', 'image3', 'image4', 'is_sale', 'sale_price', 'is_sold_out', 'is_size', 'quantity']
        labels = {
            'name': 'Product Name:',
            'price': 'Price:',
            'weight': 'Weight:',
            'category':'Category:',
            'description': 'Description:',
            'image': 'Uploade main image:',
            'image2': 'Upload a second image:',
            'image3': 'Upload a third image:',
            'image4': 'Upload a fourth image:',
            'is_sale': 'Tick box for Sale:',
            'sale_price': 'Sale Price:',
            'is_sold_out': 'Tick box for Sold Out',
            'is_size': 'Tick the box to add sizes:',
            'quantity': 'Quantity:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your product description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control image-control'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control image-control'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control image-control'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control image-control'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'is-sale form-check-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control sale-price'}),
            'is_sold_out': forms.CheckboxInput(attrs={'class': 'is-sold-out form-check-input'}),
            'is_size': forms.CheckboxInput(attrs={'class': 'is-size form-check-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-control'}),
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


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size', 'quantity', 'is_sold_out']
        labels = {
            'size': 'Add a size:',
            'quantity': 'Quantity:',
            'is_sold_out': 'Mark as sold out'
        }
        widgets = {
            'size': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Write the size (Small, Medium etc.)...' 
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_sold_out': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

SizeFormSet = inlineformset_factory(Product, Size, form=SizeForm, max_num=10, extra=10, can_delete=True)

