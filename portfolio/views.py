from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Portfolio, Image
from .forms import PortfolioForm, ImageFormSet
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def portfolio_summary(request):
    user = request.user
    if user.is_superuser:
        portfolios = Portfolio.objects.filter(is_published=True)
        if request.method == 'POST':
            for portfolio in portfolios:
                checkbox_name = f'portfolios_{portfolio.id}_is_published'
                if checkbox_name in request.POST:
                    portfolio.is_published = True
                else:
                    portfolio.is_published = False
                portfolio.save()
            messages.success(request, 'Published status updated.')    
            return redirect('portfolio_summary')
        return render(request, 'portfolio/portfolio_summary.html', {'portfolios':portfolios})
    else:
        return redirect('index')


def draft_portfolio_summary(request):
    user = request.user
    if user.is_superuser:
        portfolios = Portfolio.objects.filter(is_published=False)
        if request.method == 'POST':
            for portfolio in portfolios:
                checkbox_name = f'portfolios_{portfolio.id}_is_published'
                if checkbox_name in request.POST:
                    portfolio.is_published = True
                else:
                    portfolio.is_published = False
                portfolio.save()
            messages.success(request, 'Published status updated.')    
            return redirect('draft_portfolio_summary')
        return render(request, 'portfolio/draft_portfolio_summary.html', {'portfolios':portfolios})
    else:
        return redirect('index')


def portfolio(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    images = portfolio.image.all()
    return render(request, 'portfolio/portfolio.html', {'portfolio':portfolio, 'images':images})


def portfolio_title_page(request):
    portfolios = Portfolio.objects.filter(is_published=True)
    return render(request, 'portfolio/portfolio_title_page.html', { 'portfolios':portfolios })


def add_portfolio(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        if request.method == "POST":
            portfolio_form = PortfolioForm(request.POST, request.FILES)
            image_formset = ImageFormSet(request.POST, request.FILES)

            if portfolio_form.is_valid() and image_formset.is_valid():
                portfolio = portfolio_form.save()
                images = image_formset.save(commit=False)
                for image in images:
                    image.portfolio = portfolio
                    image.save()
                return redirect('draft_portfolio_summary')  # Redirect to a success page or similar
            else:
                return render(request, 'portfolio/add_portfolio.html', {
                    'portfolio_form': portfolio_form,
                    'image_formset': image_formset
                })
        else:
            portfolio_form = PortfolioForm()
            image_formset = ImageFormSet()
            return render(request, 'portfolio/add_portfolio.html', {
                'portfolio_form': portfolio_form,
                'image_formset': image_formset
            })
    else:
        return redirect('index')


def edit_portfolio(request, pk):
    user = request.user
    if user.is_superuser:
        portfolio = get_object_or_404(Portfolio, id=pk) 
        if request.method == 'POST':
            portfolio_form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
            image_formset = ImageFormSet(request.POST, request.FILES, instance=portfolio)
            if portfolio_form.is_valid() and image_formset.is_valid():
                updated_portfolio = portfolio_form.save()
                updated_images = image_formset.save(commit=False)
                for image in updated_images:
                    image.portfolio = updated_portfolio
                    image.save() 

               	for form in image_formset.deleted_forms: 
               		if form.instance.pk:
               			form.instance.delete()

                return redirect('index')  # Redirect to a suitable page
            else:
            	messages.error(request, 'There was an error with the forms')
            	return render(request, 'portfolio/edit_portfolio.html', {
					'portfolio': portfolio,
					'portfolio_form': portfolio_form,
					'image_formset': image_formset,
					# 'images': images  # Pass the existing images to the template
				})
        else:
            portfolio_form = PortfolioForm(instance=portfolio)
            image_formset = ImageFormSet(instance=portfolio)
        
        # Render the edit form with context
        return render(request, 'portfolio/edit_portfolio.html', {
            'portfolio': portfolio,
            'portfolio_form': portfolio_form,
            'image_formset': image_formset,
            # 'images': images

        })
    else:
        return redirect('index')


def delete_portfolio(request, pk):
    user = request.user
    porfolio = Portfolio.objects.get(id=pk)
    if user.is_superuser:
        Portfolio.objects.get(id=pk).delete()
        return redirect('portfolio_summary')
    else:
        return redirect('index')
