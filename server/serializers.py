from rest_framework import serializers
from django.contrib.auth.models import User
from store.models import Category, Book, Cart, CartItem, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']

class BookSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Book 
        fields = ['id', 'title', 'author', 'category', 'price', 'qty']


class CategorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Category 
        fields = ['id', 'name']


class CartSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Cart 
        fields = ['id', 'user']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CartItem 
        fields = ['id', 'cart', 'book', 'qty']

class OrderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Order 
        fields = ['id', 'user', 'status', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = OrderItem 
        fields = ['id', 'order', 'book', 'qty']





