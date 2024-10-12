from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField


# Create your models here.
# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'categories'


class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


# All Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = CloudinaryField('image', blank=True, null=True)
	image2 = CloudinaryField('image', blank=True, null=True)
	image3 = CloudinaryField('image', blank=True, null=True)
	image4 = CloudinaryField('image', blank=True, null=True)
	quantity = models.IntegerField(default=0)
	# Add sale stuff
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	# sold out
	is_sold_out = models.BooleanField(default=False)
	is_size = models.BooleanField(default=False, blank=True, null=True)
	# on shop floor
	is_on_shelf = models.BooleanField(default=False, blank=True, null=True)


	def __str__(self):
		return self.name


# Customer Orders
class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=10, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.product


class Size(models.Model):
	product = models.ForeignKey(Product, related_name='size', on_delete=models.CASCADE)
	size = models.CharField(max_length=150, blank=True, null=True)
	quantity = quantity = models.IntegerField(default=0)
	is_sold_out = models.BooleanField(default=False, blank=True, null=True)
	
	def __str__(self):
			return self.size