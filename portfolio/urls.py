from django.urls import path, include
from . import views

urlpatterns = [
    path('add_portfolio/', views.add_portfolio, name='add_portfolio'),
    path('draft_portfolio_summary/', views.draft_portfolio_summary, name='draft_portfolio_summary'),
    path('portfolio_summary/', views.portfolio_summary, name='portfolio_summary'),
    path('edit_portfolio/<int:pk>', views.edit_portfolio, name='edit_portfolio'),
    path('portfolio_title_page/', views.portfolio_title_page, name='portfolio_title_page'),    
    path('portfolio/<int:pk>', views.portfolio, name='portfolio'),
    path('draft_portfolio/<int:pk>', views.draft_portfolio, name='draft_portfolio'),
    path('delete_portfolio/<int:pk>/', views.delete_portfolio, name='delete_portfolio'),
]
