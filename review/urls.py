from django.urls import path, include
from . import views

urlpatterns = [
    path('write_review/', views.write_review, name='write_review'),
    path('inactive_reviews_table/', views.inactive_reviews_table, name='inactive_reviews_table'),
    path('active_reviews_table/', views.active_reviews_table, name='active_reviews_table'),
]
