from django.urls import path, include
from . import views

urlpatterns = [
    path('add_portfolio/', views.add_portfolio, name='add_portfolio'),
    path('draft_portfolio_summary/', views.draft_portfolio_summary, name='draft_portfolio_summary'),
    path('edit_portfolio/<int:pk>', views.edit_portfolio, name='edit_portfolio'),
    path('portfolio_title_page/', views.portfolio_title_page, name='portfolio_title_page'),    
]
