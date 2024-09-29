from django.db import models
import datetime
from cloudinary.models import CloudinaryField


class Portfolio(models.Model):
	title = models.CharField(max_length=250, default='', blank=True, null=True)
	description = models.TextField(max_length=500, default='', blank=True, null=True)
	is_published = models.BooleanField(default=False)
	front_image = CloudinaryField('image', blank=True, null=True)

	def __str__(self):
		return self.title if self.title else 'Untitled'

	class Meta:
		verbose_name_plural = 'galleries'

class Image(models.Model):
	portfolio = models.ForeignKey(Portfolio, related_name='image', on_delete=models.CASCADE)
	image = CloudinaryField('image', blank=True, null=True)
	caption = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return f'Image {self.id}'
