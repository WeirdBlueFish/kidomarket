from django.db import models

class Products(models.Model):
    GENDER_CHOICES = [
        ('boy', 'پسرونه'),
        ('girl', 'دخترونه'),
        ('unisex', 'اسپرت (مشترک)'),
    ]

    name = models.CharField(max_length=200, verbose_name="نام لباس")
    description = models.TextField(verbose_name="توضیحات کامل")
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