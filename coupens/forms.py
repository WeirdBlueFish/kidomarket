from django import forms
from .models import Coupon  # <--- نقطه اضافه شد

# فرم قبلی مشتریان
class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-r-xl border border-gray-300 focus:border-blue-500 outline-none text-sm',
        'placeholder': 'کد تخفیف...'
    }))

# فرم جدید برای داشبورد ادمین
class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'valid_from', 'valid_to', 'discount', 'active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }