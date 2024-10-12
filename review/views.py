from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Review
from .forms import ReviewForm
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
def write_review(request):
	if request.method == 'POST':
		review_form = ReviewForm(request.POST)
		if review_form.is_valid():
            # save review to db
			review = review_form.save(commit=False)
			review.is_active = False
			review.save()
			review_notification_email(review)
			messages.success(request, 'Thanks for leaving a review!')
			return redirect('index')
		else:
			messages.error(request, "Sorry that didn't work!")
			return render(request, 'review/write_review.html', { 'review_form':review_form })
	else:
		review_form = ReviewForm()
		return render(request, 'review/write_review.html', { 'review_form': review_form })


def review_notification_email(review):
	subject = "You have a new review to activate!"
	from_email = "j.sinclairthomson@gmail.com"
	to_email = ["j.sinclairthomson@gmail.com"] 
	html_template = get_template('review/notification.html')
	html_content = html_template.render({'review': review})
	email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
	email_message.attach_alternative(html_content, "text/html")
	email_message.send()


def inactive_reviews_table(request):
	if request.user.is_superuser:
		reviews = Review.objects.filter(is_active=False)
		if request.method == 'POST':
			for review in reviews:
				checkbox_name = f'reviews_{review.id}_is_active'
				if checkbox_name in request.POST:
					review.is_active = True
				else:
					review.is_active = False
				review.save()

			messages.success(request, 'Review status updated.')
			return redirect('inactive_reviews_table')

		return render(request, 'review/inactive_reviews_table.html', {'reviews':reviews})
	else:
		messages.error(request, 'ah ah ah what is the magic word?')
		return redirect('index')


def active_reviews_table(request):
	if request.user.is_superuser:
		reviews = Review.objects.filter(is_active=True)
		if request.method == 'POST':
			for review in reviews:
				checkbox_name = f'reviews_{review.id}_is_active'
				if checkbox_name in request.POST:
					review.is_active = True
				else:
					review.is_active = False
				review.save()
			messages.success(request, 'Review status updated.')
			return redirect('active_reviews_table')
		return render(request, 'review/active_reviews_table.html', {'reviews':reviews})
	else:
		messages.error(request, 'nope.')
		return redirect('index')