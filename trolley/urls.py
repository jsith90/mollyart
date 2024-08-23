from django.urls import path
from . import views

urlpatterns = [
    path('', views.trolley_summary, name='trolley_summary'),
    path('add/', views.trolley_add, name='trolley_add'),
    path('delete/', views.trolley_delete, name='trolley_delete'),
    path('update/', views.trolley_update, name='trolley_update'),
]