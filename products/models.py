from django.db import models

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