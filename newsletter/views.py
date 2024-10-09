from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Article, Subscriber
from .forms import CreateArticle, SubscriptionForm
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


def subscribers_dash(request):
    if request.user.is_superuser:
        subscribers = Subscriber.objects.filter(is_active=True)
        if request.method == 'POST':
            for subscriber in subscribers:
                checkbox_name = f'subscribers_{subscriber.id}_is_active'
                if checkbox_name in request.POST:
                    subscriber.is_active = True
                else:
                    subscriber.is_active = False
                subscriber.save()
            messages.success(request, 'Subscriber status updated.')    
            return redirect('subscribers_dash')
            
        return render(request, 'newsletter/subscribers_dash.html', {'subscribers':subscribers})
    else:
        messages.error(request, "Not authorised to do that bud.")
        return redirect('index')


def inactive_subscriber_dash(request):
    if request.user.is_superuser:
        subscribers = Subscriber.objects.filter(is_active=False)
        if request.method == 'POST':
            for subscriber in subscribers:
                checkbox_name = f'subscribers_{subscriber.id}_is_active'
                if checkbox_name in request.POST:
                    subscriber.is_active = True
                else:
                    subscriber.is_active = False
                subscriber.save()
            messages.success(request, 'Subscriber status updated.')    
            return redirect('inactive_subscriber_dash')
            
        return render(request, 'newsletter/inactive_subscriber_dash.html', {'subscribers':subscribers})
    else:
        messages.error(request, "Not authorised to do that bud.")
        return redirect('index')


def newsletter(request, pk):
    article = get_object_or_404(Article, id=pk)
    if article.is_published:
        return render(request, 'newsletter/newsletter.html', { 'article': article})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            subscription_email_confirmation(request, form.cleaned_data['email'])
            messages.success(request, 'Thanks for signing up to my newsletter! Check your emails for confirmation of your subscription!')
            return redirect('index')
        else:
            messages.error(request, "Sorry, that didnt work. Perhaps you're already signed up?")
            return redirect('index')
    else:
        messages.error(request, "Sorry, that didnt work.")
        return redirect('index')

    return render(request, 'newsletter/subscribe.html', {'form':form})


def subscription_email_confirmation(request, email):
    is_valid_email = True
    try:
        validate_email(email)
    except ValidationError:
        is_valid_email = False
    if is_valid_email:
        subject = "Welcome to the newsletter club!"
        from_email = "j.sinclairthomson@gmail.com"
        to_email = [email] 
        html_template = get_template('newsletter/newsletter_signup.html')
        html_content = html_template.render({'email':email})

        email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()


def newsletter_email_send(request, article):
    subscribers = Subscriber.objects.filter(is_active=True)
    invalid_emails = []
    for subscriber in subscribers:
        is_valid_email = True
        try:
            validate_email(subscriber.email)
        except ValidationError:
            is_valid_email = False
            invalid_emails.append(subscriber.email)

        if is_valid_email and subscriber.is_active:
            subject = "A Molly S-T Update!"
            from_email = "j.sinclairthomson@gmail.com"
            to_email = [subscriber.email] 
            html_template = get_template('newsletter/newsletter.html')
            html_content = html_template.render({'article':article})

            email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()
        
    if invalid_emails:
        messages.error(request, f"You have the following invalid emails in your subscriber list: {', '.join(invalid_emails)}; you should deactivate these emails.")
        return redirect('subscribers_dash')


# Create your views here.
def create_newsletter(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            article_form = CreateArticle(request.POST, request.FILES)
            if article_form.is_valid():
                # save article to db
                article = article_form.save()
                messages.success(request, 'Draft successfully created.')
                return redirect('draft_newsletter_summary')
            else:
                return render(request, 'newsletter/create_newsletter.html', { 'article_form': article_form })
        else:
            article_form = CreateArticle()
            return render(request, 'newsletter/create_newsletter.html', { 'article_form': article_form })
    else:
        return redirect('index')


def draft_newsletter(request, pk):
    user = request.user
    article = get_object_or_404(Article, id=pk)
    
    if user.is_superuser:
        if request.method == 'POST':
            # Handle the entire article form but only save is_published
            article_form = CreateArticle(request.POST, instance=article)
            if article_form.is_valid():
                # Update only the is_published field
                article.is_published = article_form.cleaned_data['is_published']
                article.save(update_fields=['is_published'])
                if article.is_published:
                    newsletter_email_send(request, article)
                    messages.success(request, "Congratulations! The world thanks you for your newsletter.")
                    return redirect('index')
        else:
            article_form = CreateArticle(instance=article)
        
        return render(request, 'newsletter/draft_newsletter.html', {
            'article': article,
            'article_form': article_form
        })
    else:
        messages.error(request, "You ain't authorised to do that bud.")
        return redirect('index')


def newsletters_summary(request):
    user = request.user
    if user.is_superuser:
        articles = Article.objects.filter(is_published=True)
        return render(request, 'newsletter/newsletters_summary.html', {'articles':articles})
    else:
        messages.error(request, "You ain't authorised to do that bud.")
        return redirect('index')

def draft_newsletter_summary(request):
    user = request.user
    if user.is_superuser:
        articles = Article.objects.filter(is_published=False)
        return render(request, 'newsletter/draft_newsletter_summary.html', {'articles':articles})
    else:
        messages.error(request, "You ain't authorised to do that bud.")
        return redirect('index')


def edit_newsletter(request, pk):
    user = request.user
    if user.is_superuser:
        article = get_object_or_404(Article, id=pk)
        if request.method == 'POST':
            article_form = CreateArticle(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                return redirect('index')  # Redirect to a suitable page
        else:
            article_form = CreateArticle(instance=article)
        
        # Render the edit form with context
        return render(request, 'newsletter/edit_newsletter.html', {
            'article': article,
            'article_form': article_form,
        })
    else:
        messages.error(request, "You ain't authorised to do that bud.")
        return redirect('index')

