from django.contrib import admin
from .models import Article, Subscriber
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Article)
admin.site.register(Subscriber)