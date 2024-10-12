from django import forms
from django.forms import inlineformset_factory
from .models import Portfolio, Image

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'is_published', 'front_image']
        labels = {
            'title': 'Gallery Title',
            'description': '',
            'is_published':'Check the box to publish gallery:',
            'front_image': 'Add a title image:',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter gallery title'}),
            'description': forms.Textarea(attrs={'class': 'form-control description', 'placeholder': 'Enter description'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'is-published'}),
            'front_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'caption']
        labels = {
            'image': 'Upload image:',
            'caption': 'Image Caption'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
            }),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter caption'}),
        }

ImageFormSet = inlineformset_factory(Portfolio, Image, form=ImageForm, max_num=None, extra=50, can_delete=True)
