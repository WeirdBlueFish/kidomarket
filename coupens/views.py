from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def apply_coupon(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    
    if form.is_valid():
        # حذف فاصله‌های اضافی قبل و بعد از کد
        code = form.cleaned_data['code'].strip()
        print(f"\n🔍 در حال بررسی کد تخفیف: '{code}'")
        print(f"⏰ زمان فعلی سرور جنگو: {now.strftime('%Y-%m-%d %H:%M')}")
        
        try:
            # ابتدا فقط چک می‌کنیم کد وجود دارد و فعال است یا خیر
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            print("✅ کد در دیتابیس پیدا شد و فعال است. در حال بررسی تاریخ...")
            
            # سپس تاریخ را دستی چک می‌کنیم تا ارور دقیق را ببینیم
            if coupon.valid_from <= now <= coupon.valid_to:
                request.session['coupon_id'] = coupon.id
                print(f"🎉 تخفیف {coupon.discount} درصدی با موفقیت در سشن ذخیره شد!")
            else:
                request.session['coupon_id'] = None
                print(f"❌ خطای تاریخ: کد منقضی شده یا هنوز شروع نشده است.")
                print(f"   شروع اعتبار کد: {coupon.valid_from.strftime('%Y-%m-%d %H:%M')}")
                print(f"   پایان اعتبار کد: {coupon.valid_to.strftime('%Y-%m-%d %H:%M')}")
                
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            print("❌ خطا: این کد در دیتابیس وجود ندارد یا تیک 'فعال' آن خاموش است.")
    else:
        print("❌ خطا در فرم:", form.errors)
        
    return redirect('cart_detail')