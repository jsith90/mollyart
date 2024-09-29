from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Commission, Image, Past_Commission_Image
from .forms import CommissionForm, ImageForm, ImageFormSet, Past_Commission_ImageForm
from review.models import Review
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.http import HttpResponse
import logging
import time
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# Create your views here.
def create_commission(request):
	past_images = Past_Commission_Image.objects.filter(is_active=True)
	reviews = Review.objects.filter(is_active=True)
	if request.method == 'POST':
		commission_form = CommissionForm(request.POST)
		image_formset = ImageFormSet(request.POST, request.FILES)
		if commission_form.is_valid() and image_formset.is_valid():
            # save article to db
			commission = commission_form.save()
			images = image_formset.save(commit=False)
			for image in images:
				image.commission = commission
				image.save()
			commission_email(commission, images)
			messages.success(request, "Thanks for sending your commission proposal! I'll be in touch soon about your idea.")
			return redirect('index')
		else:
			messages.error(request, "Something's up with your form.")
			return render(request, 'commission/create_commission.html', { 'reviews': reviews, 'commission_form':commission_form, 'image_formset': image_formset, 'past_images':past_images })
	else:
		commission_form = CommissionForm()
		image_formset = ImageFormSet()
		return render(request, 'commission/create_commission.html', { 'reviews': reviews, 'commission_form': commission_form, 'image_formset': image_formset, 'past_images': past_images })


def commission_email(commission, images):
	subject = "A new commission"
	from_email = "j.sinclairthomson@gmail.com"
	to_email = ["j.sinclairthomson@gmail.com"] 
	html_template = get_template('commission/commission.html')
	html_content = html_template.render({'commission': commission, 'images': images})
	email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
	email_message.attach_alternative(html_content, "text/html")
	email_message.send()



def order_shipped_email(request, order):
	items = OrderItem.objects.filter(order=order)
	order_email = order.email
	is_valid_email = True
	try:
		validate_email(order_email)
	except ValidationError:
		is_valid_email = False
	if is_valid_email:
		subject = "Your order has been shipped!"
		from_email = "j.sinclairthomson@gmail.com"
		to_email = [order_email] 
		html_template = get_template('payment/shipped_email.html')
		html_content = html_template.render({'order': order, 'items': items})
		email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
		email_message.attach_alternative(html_content, "text/html")
		email_message.send()
		messages.success(request, 'An order email has been sent!')
	else:
		messages.error(request, 'The email address was invalid and and a shipping confirmation could not be sent.')
		return redirect('not_shipped_dash')



def old_commission_image_upload(request):
	user = request.user
	if user.is_superuser:
		if request.method == 'POST':
			past_commission_form = Past_Commission_ImageForm(request.POST, request.FILES)
			if past_commission_form.is_valid():
				commission_image = past_commission_form.save(commit=False)
				commission_image.is_active = True
				commission_image.save()
				messages.success(request, "You've added a new image to the database, now be sure to activate it as well!")
				return redirect('admin_dash')
			else:
				return render(request, 'commission/old_commission_image_upload.html', { 'past_commission_form': past_commission_form })
		else:
			past_commission_form = Past_Commission_ImageForm()
			return render(request, 'commission/old_commission_image_upload.html', { 'past_commission_form': past_commission_form })

	else:
		messages.error (request, "Not authorised to do that bud.")
		return redirect('index')

def image_reel_dash(request):
    if request.user.is_superuser:
        images = Past_Commission_Image.objects.filter(is_active=True)
        if request.method == 'POST':
            for image in images:
                checkbox_name = f'images_{image.id}_is_active'
                if checkbox_name in request.POST:
                    image.is_active = True
                else:
                    image.is_active = False
                image.save()
            messages.success(request, 'Image status updated.')    
            return redirect('image_reel_dash')
            
        return render(request, 'commission/image_reel_dash.html', { 'images':images })
    else:
        messages.error(request, "Not authorised to do that bud.")
        return redirect('index')

def inactive_image_reel_dash(request):
    if request.user.is_superuser:
        images = Past_Commission_Image.objects.filter(is_active=False)
        if request.method == 'POST':
            for image in images:
                checkbox_name = f'images_{image.id}_is_active'
                if checkbox_name in request.POST:
                    image.is_active = True
                else:
                    image.is_active = False
                image.save()
            messages.success(request, 'Image status updated.')    
            return redirect('inactive_image_reel_dash')
            
        return render(request, 'commission/inactive_image_reel_dash.html', { 'images':images })
    else:
        messages.error(request, "Not authorised to do that bud.")
        return redirect('index')

