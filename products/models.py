from django.db import models
import jdatetime
from django.contrib.auth.models import User

class Products(models.Model):
    GENDER_CHOICES = [
        ('boy', 'پسرونه'),
        ('girl', 'دخترونه'),
        ('unisex', 'اسپرت (مشترک)'),
    ]

    name = models.CharField(max_length=200, verbose_name="نام لباس")
    description = models.TextField(verbose_name="توضیحات کامل")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="دسته بندی")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="دسته‌بندی")
    min_age = models.PositiveIntegerField(verbose_name="حداقل سن (سال)", default=1)
    max_age = models.PositiveIntegerField(verbose_name="حداکثر سن (سال)", default=16)
    stock = models.PositiveIntegerField(verbose_name="موجودی در انبار", default=0)
    is_active = models.BooleanField(default=True, verbose_name="فعال برای فروش")
    image = models.ImageField(upload_to='products/%Y/%m/', verbose_name="عکس لباس", null=True, blank=True)
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته بندی')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name='زیرشاخه')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '->'.join(full_path[::1])

    def get_all_descendants(self):
        descendant_ids = [self.id]

        for child in self.subcategories.all():
            descendant_ids.extend(child.get_all_descendants())
        return descendant_ids

class ProductSize(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='sizes', verbose_name='لباس')
    name = models.CharField(max_length=50, verbose_name='نام سایز')

    price = models.PositiveIntegerField(verbose_name='قیمت (تومان)', default=0)
    stock = models.PositiveIntegerField(verbose_name='موجودی', default=0)


    min_height = models.PositiveIntegerField(blank=True, null=True, verbose_name="حداقل قد کودک (سانتی‌متر)")
    max_height = models.PositiveIntegerField(blank=True, null=True, verbose_name="حداکثر قد کودک (سانتی‌متر)")
    
    features = models.TextField(blank=True, null=True, verbose_name="ویژگی‌های ابعاد", help_text="هر ویژگی را در یک خط بنویسید. مثلاً: قد آستین: 40 سانتی‌متر")

    class Meta:
        verbose_name = 'سایز و ابعاد'
        verbose_name_plural = 'سایزها و ابعاد'

    def __str__(self):
        return f"{self.name} - {self.product.name}"

class Comment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    name = models.CharField(max_length=50, verbose_name="نام شما")
    body = models.TextField(verbose_name="متن نظر")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_active = models.BooleanField(default=False, verbose_name="تایید شده / نمایش داده شود؟")

    rating = models.PositiveSmallIntegerField(default=5, verbose_name="امتیاز")

    class Meta:
        ordering = ('-created',)
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"نظر {self.name} روی {self.product.name}"

    def get_jalali(self):
            jalali_date = jdatetime.datetime.fromgregorian(datetime=self.created)
            return jalali_date.strftime("%Y/%m/%d")
    
    get_jalali.short_description = "تاریخ ثبت (شمسی)"

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    
    def __str__(self):
        return f"عکس برای {self.product.name}"

class StockNotification(models.Model):
    size = models.ForeignKey('ProductSize', on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False, verbose_name="اطلاع‌رسانی شده")

    def __str__(self):
        return f"{self.phone} - {self.size.product.name} ({self.size.name})"