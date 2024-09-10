from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Article(models.Model):
	title = models.CharField(max_length=250, default='', blank=True, null=True)
	body = models.TextField(default='', blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	image1 = CloudinaryField('image1', blank=True, null=True)
	caption1 = models.CharField(max_length=200, blank=True, null=True)
	image2 = CloudinaryField('image2', blank=True, null=True)
	caption2 = models.CharField(max_length=200, blank=True, null=True)
	image3 = CloudinaryField('image3', blank=True, null=True)
	caption3 = models.CharField(max_length=200, blank=True, null=True)
	image4 = CloudinaryField('image4', blank=True, null=True)
	caption4 = models.CharField(max_length=200, blank=True, null=True)
	is_published = models.BooleanField(default=False)

	def __str__(self):
		return self.title if self.title else 'Untitled'


	def snippet(self):
		return self.body[:50] + '...'


class Subscriber(models.Model):
	email = models.EmailField(unique=True)
	subscribed_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.email