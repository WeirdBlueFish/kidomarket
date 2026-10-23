from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 
    can_delete = False

    readonly_fields = ('product', 'product_size', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_jalali', 'paid')
    
    list_filter = ['paid', 'created']
    
    search_fields = ['first_name', 'last_name', 'phone']
    
    inlines = [OrderItemInline]