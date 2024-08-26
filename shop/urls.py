"""
URL configuration for mollyart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('shop/', views.shop, name="shop"),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<str:foo>/', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_update/<int:product_id>/', views.product_update, name='product_update'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_update/<int:category_id>/', views.category_update, name='category_update'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('delete_category/<int:pk>', views.delete_category, name='delete_category'),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout"),
]
