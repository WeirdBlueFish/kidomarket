from django.contrib import admin
from .models import Products, Category, ProductSize

# Register your models here.
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_age', 'max_age', 'price', 'stock', 'is_active']
    list_filter = ('gender', 'is_active')
    search_fields = ('name',)
    inlines = [ProductSizeInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)