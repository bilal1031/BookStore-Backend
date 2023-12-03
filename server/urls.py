"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login",views.login, name="login"),
    path("signup",views.signup, name="signup"),

    
    path("category", views.list_categories, name="list_categories"),
    path("category/add", views.create_category, name="create_category"),
    path("category/<int:id>/", views.get_category, name="get_category"),
    path("category/<int:id>/update", views.update_category, name="update_category"),
    path("category/<int:id>/delete", views.delete_category, name="delete_category"),

    path("book", views.list_books, name="list_books"),
    path("book/add", views.create_book, name="create_book"),
    path("book/<int:id>/", views.get_book, name="get_book"),
    path("book/<int:id>/update", views.update_book, name="update_book"),
    path("book/<int:id>/delete", views.delete_book, name="delete_book"),
    
    path("cart/add", views.create_cart, name="create_cart"),
    path("cart/<int:id>/", views.get_cart, name="get_cart"),
    path("cart/<int:id>/update", views.update_cart, name="update_cart"),
    path("cart/<int:id>/delete", views.delete_cart, name="delete_cart"),

    path("order/add", views.create_order, name="create_order"),
    path("order/<int:id>/", views.get_order, name="get_order"),
    # path("order/<int:id>/update", views.update_order, name="update_order"),
    # path("order/<int:id>/delete", views.delete_order, name="delete_order"),
]