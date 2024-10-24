from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name (required)'}), required=True)
	shipping_email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email (required)'}), required=True)
	shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1 (required)'}), required=True)
	shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
	shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City (required)'}), required=True)
	shipping_region = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Region (required)'}), required=True)
	shipping_postcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Postcode (required)'}), required=True)
	shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'value':'United Kingdom', 'readonly':'readonly','class':'form-control', 'placeholder':'country (required)'}), required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_region', 'shipping_postcode', 'shipping_country',]