from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value):
    if value:
        # تبدیل تاریخ میلادی دیتابیس به تاریخ شمسی
        jalali_date = jdatetime.date.fromgregorian(date=value)
        # نمایش به فرمت 1402/05/12
        return f"{jalali_date.year}/{jalali_date.month:02d}/{jalali_date.day:02d}"
    return ""