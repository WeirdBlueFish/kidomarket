from django.contrib import admin
from .models import Products

# Register your models here.

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'min_age', 'max_age', 'price', 'stock', 'is_active']
    list_filter = ('gender', 'is_active')
    search_fields = ('name',)