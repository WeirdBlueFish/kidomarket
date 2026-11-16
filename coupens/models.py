from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="کد تخفیف")
    valid_from = models.DateTimeField(verbose_name="معتبر از تاریخ")
    valid_to = models.DateTimeField(verbose_name="معتبر تا تاریخ")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف"
    )
    active = models.BooleanField(default=True, verbose_name="وضعیت فعالیت")

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"

    def __str__(self):
        return self.code