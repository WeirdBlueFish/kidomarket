from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="کاربر")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تماس")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس کامل")

    def __str__(self):
        return f"پروفایل {self.user.username}"


class Child(models.Model):
    GENDER_CHOICES = (
        ('boy', 'پسر'),
        ('girl', 'دختر'),
    )
    BODY_TYPE_CHOICES = (
        ('slim', 'لاغر'),
        ('normal', 'معمولی'),
        ('chubby', 'تپل'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children', verbose_name="والد")
    name = models.CharField(max_length=50, verbose_name="نام فرزند")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='boy', verbose_name="جنسیت")
    birth_date = models.DateField(verbose_name="تاریخ تولد (میلادی جهت محاسبات)")

    # ابعاد فیزیکی و تیپ بدنی برای سایزبندی دقیق‌تر لباس
    height = models.PositiveIntegerField(blank=True, null=True, verbose_name="قد (سانتی‌متر)")
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name="وزن (کیلوگرم)")
    chest = models.PositiveIntegerField(blank=True, null=True, verbose_name="دور سینه (سانتی‌متر)")
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, default='normal', verbose_name="جثه / تیپ بدنی")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return f"{self.name} (فرزند {self.user.username})"

    def get_age(self):
        today = timezone.now().date()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return max(age, 0)

    def needs_update(self):
        if not self.updated_at:
            return False
        return (timezone.now() - self.updated_at).days >= 120

    def _closest_birthday(self):
        today = timezone.now().date()
        candidates = []
        for year in (today.year - 1, today.year, today.year + 1):
            try:
                candidates.append(datetime.date(year, self.birth_date.month, self.birth_date.day))
            except ValueError:
                # مدیریت سال کبیسه (۲۹ فوریه)
                candidates.append(datetime.date(year, 2, 28))
        return min(candidates, key=lambda d: abs((d - today).days))

    def get_or_create_birthday_coupon(self, discount_percent=15):
        """
        اگر بین ۷ روز قبل تا ۳ روز بعد از تولد کودک باشیم،
        کد تخفیف اختصاصی همان سال را می‌سازد یا برمی‌گرداند.
        """
        today = timezone.now().date()
        bday = self._closest_birthday()
        diff_days = (bday - today).days

        if -3 <= diff_days <= 7:
            from coupens.models import Coupon
            code = f"BDAY-{self.id}-{bday.year}"
            now = timezone.now()
            valid_to = now + datetime.timedelta(days=10)

            coupon, _ = Coupon.objects.get_or_create(
                code=code,
                defaults={
                    'valid_from': now - datetime.timedelta(minutes=5),
                    'valid_to': valid_to,
                    'discount': discount_percent,
                    'active': True,
                }
            )
            if coupon.active and coupon.valid_to >= now:
                return coupon
        return None