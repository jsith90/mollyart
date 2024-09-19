from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.db.models import Q
import json
from django.contrib.auth import authenticate, login, logout
from trolley.trolley import Trolley
from newsletter.forms import SubscriptionForm
from newsletter.views import subscribe
from newsletter.models import Article
from review.models import Review


# login page
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})

# logs users out
def logout_user(request):
    logout(request)
    return redirect('index')


# Create your views here.
def index(request):
	reviews = Review.objects.filter(is_active=True)
	return render(request, 'index.html', { 'reviews':reviews })

def admin_dash(request):
	user = request.user
	if user.is_superuser:
		return render(request, 'admin.html', {})
	else:
		return redirect('index')

def shop(request):
	products = Product.objects.all()
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
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category, 'categories':categories})
	except:
		messages.error(request, ('Nothing available here at the moment.'))
		return redirect('index')


def product(request, pk):
	product = Product.objects.get(id=pk)
	categories = Category.objects.all()
	trolley = Trolley(request)
	return render(request, 'product.html', {'product':product, 'trolley':trolley, 'categories':categories})


def add_product(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)           
            if product_form.is_valid():
                # save product to db
                product = product_form.save()
                return redirect('index')
            else:
                return render(request, 'add_product.html', { 'product_form': product_form })
        else:
            product_form = ProductForm()
            return render(request, 'add_product.html', { 'product_form': product_form })
    else:
        return redirect('index')


# Create your views here.
def product_update(request, product_id):
	user = request.user
	if user.is_superuser:
		product = get_object_or_404(Product, id=product_id)
		if request.method == 'POST':
			product_form = ProductForm(request.POST, request.FILES, instance=product)
			if product_form.is_valid():
				product_form.save()
				return redirect('index')
			# Redirect to a suitable page after updating
			else:
				return render(request, 'product_update.html', { 'product':product, 'product_form': product_form, 'product': product})
		else:
			product_form = ProductForm(instance=product)
			return render(request, 'product_update.html', { 'product': product, 'product_form': product_form })
	else:
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
		return redirect('index')


def delete_product(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    if user.is_superuser:
        Product.objects.get(id=pk).delete()
        return redirect('shop')
    else:
    	return redirect('index')


def delete_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if user.is_superuser:
        Category.objects.get(id=pk).delete()
        return redirect('shop')
    else:
    	return redirect('index')