from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="کاربر")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تماس")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس کامل")
    
    def __str__(self):
        return f"پروفایل {self.user.username}"

class Child(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children', verbose_name="والد")
    name = models.CharField(max_length=50, verbose_name="نام فرزند")
    birth_date = models.DateField(verbose_name="تاریخ تولد (میلادی جهت محاسبات)")
    
    # ابعاد فیزیکی برای سایزبندی دقیق‌تر لباس
    height = models.PositiveIntegerField(blank=True, null=True, verbose_name="قد (سانتی‌متر)")
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name="وزن (کیلوگرم)")
    chest = models.PositiveIntegerField(blank=True, null=True, verbose_name="دور سینه (سانتی‌متر)")
    
    def __str__(self):
        return f"{self.name} (فرزند {self.user.username})"