from django.shortcuts import redirect, render, get_object_or_404
from products.models import Products, ProductSize
from .cart import Cart
from coupens.forms import CouponApplyForm # ایمپورت فرم

# Create your views here.

def cart_add(request, product_id):
    cart = Cart(request)
    # جستجو بر اساس کلاس Products انجام شود
    product = get_object_or_404(Products, id=product_id) 
    
    size_id = request.POST.get('size_id')
    
    if size_id:
        size = get_object_or_404(ProductSize, id=size_id, product=product)
        cart.add(product=product, size=size)
        
    # آدرس برگشت به صفحه سبد خرید (نام آن را با urls.py خود چک کنید)
    return redirect('cart_detail')


# دقت کنید که ورودی تابع از product_id به size_id تغییر کرد
def cart_remove(request, size_id):
    cart = Cart(request)
    cart.remove(size_id)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    })