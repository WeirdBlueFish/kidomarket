from django.contrib import admin
from .models import Products, Category

# Register your models here.

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'min_age', 'max_age', 'price', 'stock', 'is_active']
    list_filter = ('gender', 'is_active')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)