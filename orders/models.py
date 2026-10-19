from django.db import models
from django.contrib.auth.models import User
from products.models import Products

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس دقیق")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    paid = models.BooleanField(default=False, verbose_name="پرداخت شده")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True, verbose_name='کاربر سایت')
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"سفارش شماره {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name="قیمت")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return str(self.id)