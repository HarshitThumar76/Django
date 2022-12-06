from django.contrib import admin
from .models import Order, OrderUpdate, Product, Contact, Comments

# Register your models here.
admin.site.register((Product, Contact, Order, OrderUpdate, Comments))
