from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

# Create your models here.
class Review(models.Model):
	name = models.CharField(max_length=50)
	review = models.TextField(max_length=300)
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.name if self.name else 'Untitled'