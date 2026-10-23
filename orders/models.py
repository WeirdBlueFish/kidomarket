from django.db import models
from django.contrib.auth.models import User
from products.models import Products, ProductSize
import jdatetime

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

    def get_jalali(self):
        jalali_date = jdatetime.datetime.fromgregorian(datetime=self.created)
        return jalali_date.strftime("%Y/%m/%d")

    get_jalali.short_description = "تاریخ ثبت (شمسی)"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name="قیمت")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    product_size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, verbose_name="سایز انتخابی")

    def __str__(self):
        return str(self.id)