from django.urls import path, include
from . import views


urlpatterns = [
    path('create_newsletter/', views.create_newsletter, name='create_newsletter'),
    path('draft_newsletter/<int:pk>/', views.draft_newsletter, name='draft_newsletter'),
    path('newsletter/<int:pk>/', views.newsletter, name="newsletter"),
    path('edit_newsletter/<int:pk>/', views.edit_newsletter, name='edit_newsletter'),
    path('newsletters_summary/', views.newsletters_summary, name='newsletters_summary'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribers_dash/', views.subscribers_dash, name="subscribers_dash" )
]
