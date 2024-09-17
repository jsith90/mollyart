from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Image, Past_Commission_Image

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['name', 'email', 'address', 'commission_title', 'commission_idea', 'canvas_size', 'deadline_date', 'contact_number', 'framing_options']
        labels = {
            'name': 'Your Name (required):',
            'email': 'Email (required):',
            'address': 'Address (for delivery quote estimation | required):',
            'commission_title': 'Commission Name (required):',
            'commission_idea':'Commission Idea (required):',
            'canvas_size': 'Canvas Size:',
            'deadline_date': 'Deadline Date (required):',
            'contact_number': 'Contact Number:',
            'framing_options': 'Framing Options:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name...', 'required': 'required'}),
        	'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address...', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your delivery address...', 'required': 'required'}),
            'commission_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your commission title...', 'required': 'required'}),
            'commission_idea': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your idea...', 'required': 'required'}),
            'canvas_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your sizes...'}),
            'deadline_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number...'}),
            'framing_options': forms.Select(attrs={'class': 'form-control'}),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        labels = {
            'image': 'Upload an image:'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
            }),
        }

ImageFormSet = inlineformset_factory(Commission, Image, form=ImageForm, max_num=10, extra=10, can_delete=True)


class Past_Commission_ImageForm(forms.ModelForm):
	class Meta:
		model = Past_Commission_Image
		fields = ['image_name', 'image', 'is_active']
		labels = {
			'image_name': 'Image Title:',
			'image': 'Upload your image:',
			'is_active': 'Your commission image status:'
		}
		widgets = {
			'image_name': forms.TextInput(attrs={'class': 'form-control'}),
			'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
			'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}