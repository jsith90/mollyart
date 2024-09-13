from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField


class Commission(models.Model):
	FRAMING_OPTIONS = [
		('n/a', 'N/A'),
		('behind glass', 'Behind Glass'),
		('tray frame', 'Tray Frame'),
	]

	email = models.EmailField(max_length=250)
	address = models.TextField(max_length=15000)
	commission_title = models.CharField(max_length=250)
	commission_idea = models.TextField(max_length=100000)
	canvas_size = models.CharField(max_length=250, default='', blank=True, null=True)
	deadline_date = models.DateField(blank=True, null=True)
	contact_number = models.CharField(max_length=15, blank=True, null=True)
	framing_options = models.CharField(max_length=20, choices=FRAMING_OPTIONS, default='n/a')


	def __str__(self):
		return self.commission_title if self.commission_title else 'Untitled'

class Image(models.Model):
	commission = models.ForeignKey(Commission, related_name='image', on_delete=models.CASCADE)
	image = CloudinaryField('image', blank=True, null=True)

	def __str__(self):
		return f'Image {self.id}'


class Past_Commission_Image(models.Model):
	image_name = models.CharField(max_length=250)
	image = CloudinaryField('image')
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.image_name if self.image_name else 'Untitled'