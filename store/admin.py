from django.contrib import admin
from .models import Category, Product, Wilaya, Commune, Order, OrderItem

# Register your models here.

admin.site.register([Category, Product, Wilaya, Commune, Order, OrderItem])