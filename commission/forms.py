from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Image, Past_Commission_Image
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class CommissionForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="Are you a Bot?")
    
    class Meta:
        model = Commission
        fields = ['name', 'email', 'address', 'commission_title', 'commission_idea', 'medium', 'canvas_size', 'other_info', 'deadline_date', 'contact_number',]
        labels = {
            'name': 'Your Name (required):',
            'email': 'Email (required):',
            'address': 'Address (for delivery quote estimation | required):',
            'commission_title': 'Commission Name (required):',
            'commission_idea':'Commission Idea (required):',
            'medium':'Medium (drop-down | required):',
            'canvas_size': 'Canvas Size:',
            'other_info': 'More Info (required):',
            'deadline_date': 'Deadline Date (required):',
            'contact_number': 'Contact Number:',
            'framing_options': 'Framing Options (drop-down):',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your name here...', 'required': 'required'}),
        	'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Write your email here...', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your address here...', 'required': 'required'}),
            'commission_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your commission title here...', 'required': 'required'}),
            'commission_idea': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your commission ideas here...', 'required': 'required'}),
            'medium': forms.Select(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Select an option'}),
            'canvas_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write the sizes you want here...'}),
            'other_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'If you select other, please specify further...'}),
            'deadline_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your number here...'}),
            'framing_options': forms.Select(attrs={'class': 'form-control'}),
        }

    # Override the medium field to add an empty choice
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medium'].choices = [('', 'Select an option')] + list(self.fields['medium'].choices)


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