from django import forms
from .models import Article, Subscriber


class CreateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image1', 'caption1', 'image2', 'caption2', 'image3', 'caption3', 'image4', 'caption4', 'is_published']
        labels = {
            'title': 'Newsletter Title:',
            'body': 'Newsletter Content:',
            'image1':'Upload image:',
            'caption1': 'Add Caption:',
            'image2': 'Upload a second image:',
            'caption2': 'Add Caption:',
            'image3': 'Upload a third image:',
            'caption3': 'Add Caption:',
            'image4': 'Upload a fourth image:',
            'caption4': 'Add Caption:',
            'is_published':'Check the box before posting the newsletter:'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter newsletter title...'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your newsletter here...'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter caption'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter caption'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter caption'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter caption'}),
            'is_published': forms.CheckboxInput(),
        }


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        labels = {
            'email': 'Subscribe to my newsletter:'
        }
        widgets = {
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter your email...', 'required': 'required'}),
        }