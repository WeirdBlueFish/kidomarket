from django.contrib import admin
from .models import Products, Category, ProductSize, Comment, ProductImage

# Register your models here.
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_age', 'max_age', 'price', 'stock', 'is_active']
    list_filter = ('gender', 'is_active')
    search_fields = ('name',)
    # اضافه کردن اینلاین عکس‌ها در کنار سایزها
    inlines = [ProductSizeInline, ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created', 'is_active')
    list_filter = ('is_active', 'created')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
    approve_comments.short_description = "تایید نظرات انتخاب شده"