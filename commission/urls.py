from django.urls import path, include
from . import views

urlpatterns = [
    path('create_commission/', views.create_commission, name='create_commission'),
    path('old_commission_image_upload/', views.old_commission_image_upload, name='old_commission_image_upload'),
    path('image_reel_dash/', views.image_reel_dash, name="image_reel_dash" ),
    path('inactive_image_reel_dash/', views.inactive_image_reel_dash, name="inactive_image_reel_dash" ),
]
