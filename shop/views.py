from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Size
from .forms import ProductForm, CategoryForm, SizeFormSet, SizeForm
from django.contrib import messages
from django.db.models import Q
import json
from django.contrib.auth import authenticate, login, logout
from trolley.trolley import Trolley
from newsletter.forms import SubscriptionForm
from newsletter.views import subscribe
from newsletter.models import Article
from review.models import Review
from portfolio.models import Portfolio
from django.forms import inlineformset_factory
from django.db.models import F 

# login page
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dash')
        else:
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})

# logs users out
def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('index')

# Create your views here.
def index(request):
	reviews = Review.objects.filter(is_active=True)
	portfolios = Portfolio.objects.filter(is_published=True)
	return render(request, 'index.html', { 'reviews':reviews, 'portfolios':portfolios })

# Create your views here.
def about(request):
	return render(request, 'about.html', {})


def admin_dash(request):
	user = request.user
	if user.is_superuser:
		return render(request, 'admin.html', {})
	else:
		messages.error(request, 'You do not have access.')
		return redirect('index')


def shop(request):
	displayed_items = Product.objects.filter(is_on_shelf=True)
	products = displayed_items.order_by(
		F('is_sold_out').asc(),
		F('is_sale').asc()
	)
	categories = Category.objects.all()
	return render(request, 'shop.html', {'products':products, 'categories':categories})


def search(request):
	# determine if they fill out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# query the product db model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# return for null
		if not searched:
			messages.error(request, "Sorry that probably doesn't exist round these parts.")
			return render(request, 'search.html', {})
		else:
			return render(request, 'search.html', {'searched':searched})
	else:
		return render(request, 'search.html', {})


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {'categories':categories})


def category(request, foo):
	categories = Category.objects.all()
	# replace hyphens with spaces
	foo = foo.replace('-', ' ')
	# grab category from url
	try:
		category = Category.objects.get(name=foo)
		displayed_items = Product.objects.filter(category=category, is_on_shelf=True)
		products = displayed_items.order_by(
			F('is_sold_out').asc(),
			F('is_sale').asc()
		)
		return render(request, 'category.html', {'products':products, 'category':category, 'categories':categories})
	except:
		messages.error(request, ('Nothing available here at the moment.'))
		return redirect('index')


def product(request, pk):
	product = Product.objects.get(id=pk)
	sizes = product.size.all() 
	categories = Category.objects.all()
	trolley = Trolley(request)
	product_ids = trolley.get_product_ids()
	if product.is_on_shelf:
		if product.is_size:
			if all(size.is_sold_out for size in sizes):
				product.is_sold_out = True
				product.save()
		return render(request, 'product.html', {'product_ids':product_ids, 'product':product, 'sizes':sizes, 'trolley':trolley, 'categories':categories})
	else:
		messages.error(request, 'That product is currently unavailable.')
		return redirect('shop')

def warehoused_product(request, pk):
	user = request.user
	product = Product.objects.get(id=pk)
	sizes = product.size.all() 
	categories = Category.objects.all()
	if user.is_superuser:
		if not product.is_on_shelf:
			if product.is_size:
				if all(size.is_sold_out for size in sizes):
					product.is_sold_out = True
					product.save()
			return render(request, 'warehoused_product.html', {'product':product, 'sizes':sizes, 'categories':categories})
		else:
			messages.error(request, 'That product is currently unavailable.')
			return redirect('shop')
	else:
		messages.error(request, 'You not authorised in here, get out!')
		return redirect('shop')

def add_product(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)
            size_formset = SizeFormSet(request.POST, request.FILES)         
            if product_form.is_valid() and size_formset.is_valid():
                # save product to db
                product = product_form.save()
                sizes = size_formset.save(commit=False)
                for size in sizes:
                	size.product = product
                	size.save()
                messages.success(request, 'Product added to warehouse.')
                return redirect('warehoused_product_summary')
            else:
            	messages.error(request, 'There was an error and the product was not created')
            	return render(request, 'add_product.html', { 'product_form': product_form, 'size_formset': size_formset })
        else:
            product_form = ProductForm()
            size_formset = SizeFormSet()
            return render(request, 'add_product.html', { 'product_form': product_form, 'size_formset': size_formset })
    else:
    	messages.error(request, 'Beware of the guard dog.')
    	return redirect('index')

# Create your views here.
def product_update(request, product_id):
	user = request.user
	if user.is_superuser:
		product = get_object_or_404(Product, id=product_id)
		sizes = product.size.all()
		if request.method == 'POST':
			product_form = ProductForm(request.POST, request.FILES, instance=product)
			size_formset = SizeFormSet(request.POST, request.FILES, instance=product)     
			if product_form.is_valid() and size_formset.is_valid():
				product_form.save()
				sizes = size_formset.save(commit=False)
				for size in sizes:
					size.product = product
					size.save()

				for form in size_formset.deleted_forms:
					if form.instance.product_id:
						form.instance.delete()
				messages.success(request, 'Product updated!')
				return redirect('products_summary')
			# Redirect to a suitable page after updating
			else:
				print("Product form errors:", product_form.errors)
				print("Size formset errors:", size_formset.errors)
				messages.error(request, 'There was an error with the update.')
				return render(request, 'product_update.html', { 'product':product, 'product_form': product_form, 'size_formset': size_formset })
		else:
			product_form = ProductForm(instance=product)
			size_formset = SizeFormSet(instance=product) 
			return render(request, 'product_update.html', { 'product': product, 'product_form': product_form, 'size_formset': size_formset })
	else:
		messages.error(request, 'You do not have the right permit to enter this room.')
		return redirect('index')


def add_category(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            category_form = CategoryForm(request.POST, request.FILES)           
            if category_form.is_valid():
                # save category to db
                category = category_form.save()
                return redirect('shop')
            else:
                return render(request, 'add_category.html', { 'category_form': category_form })
        else:
            category_form = CategoryForm()
            return render(request, 'add_category.html', { 'category_form': category_form })
    else:
    	messages.error(request, 'Get out!')
    	return redirect('index')

# Create your views here.
def category_update(request, category_id):
	user = request.user
	if user.is_superuser:
		category = get_object_or_404(Category, id=category_id)
		if request.method == 'POST':
			category_form = CategoryForm(request.POST, request.FILES, instance=category)
			if category_form.is_valid():
				category_form.save()
				return redirect('index')
			# Redirect to a suitable page after updating
			else:
				return render(request, 'category_update.html', { 'category':category, 'category_form': category_form, 'category': category})
		else:
			category_form = CategoryForm(instance=category)
			return render(request, 'category_update.html', { 'category': category, 'category_form': category_form })
	else:
		messages.error(request, 'No authorisation to do that.')
		return redirect('index')


def delete_product(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    if user.is_superuser:
        Product.objects.get(id=pk).delete()
        messages.success(request, 'Product deleted.')
        return redirect('shop')
    else:
    	messages.error(request, 'Sorry old boy, you cannot do that here.')
    	return redirect('index')


def delete_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if user.is_superuser:
        Category.objects.get(id=pk).delete()
        messages.success(request, 'Category deleted.')
        return redirect('shop')
    else:
    	messages.error(request, 'Ah ah ah, you did not say the magic word.')
    	return redirect('index')


def products_summary(request):
    user = request.user
    if user.is_superuser:
        products = Product.objects.filter(is_on_shelf=True)
        if request.method == 'POST':
            for product in products:
                checkbox_name = f'products_{product.id}_is_on_shelf'
                if checkbox_name in request.POST:
                    product.is_on_shelf = True
                else:
                    product.is_on_shelf = False
                product.save()
            messages.success(request, 'Product status updated.')    
            return redirect('products_summary')
        return render(request, 'products_summary.html', {'products':products})
    else:
    	messages.error(request, 'Ah ah ah, you did not say the magic word.')
    	return redirect('index')


def warehoused_product_summary(request):
    user = request.user
    if user.is_superuser:
        products = Product.objects.filter(is_on_shelf=False)
        if request.method == 'POST':
            for product in products:
                checkbox_name = f'products_{product.id}_is_on_shelf'
                if checkbox_name in request.POST:
                    product.is_on_shelf = True
                else:
                    product.is_on_shelf = False
                product.save()
            messages.success(request, 'Product status updated.')    
            return redirect('warehoused_product_summary')
        return render(request, 'warehoused_product_summary.html', {'products':products})
    else:
        return redirect('index')

