from django.contrib import admin
from .models import Commission, Image, Past_Commission_Image
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Commission)
admin.site.register(Image)
admin.site.register(Past_Commission_Image)