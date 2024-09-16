from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['name', 'review', 'is_active']
		labels = {
			'name': 'Your first name:',
			'review': 'Review:',
			'is_active': "This review's status:",
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
			'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your thoughts...', 'required':'required'}),
			'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}