from django.shortcuts import redirect, render, get_object_or_404
from products.models import Products, ProductSize
from django.views.decorators.http import require_POST
from .cart import Cart
from coupens.forms import CouponApplyForm # ایمپورت فرم
from django.contrib import messages

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

@require_POST
def cart_update(request, size_id):
    cart = Cart(request)
    size = get_object_or_404(ProductSize, id=size_id)
    action = request.POST.get('action')
    current_qty = cart.cart.get(str(size_id), {}).get('quantity', 0)

    if action == 'increase':
        if current_qty + 1 <= size.stock:
            cart.add(product=size.product, size=size, quantity=current_qty + 1, override_quantity=True)
        else:
            messages.warning(request, f'حداکثر موجودی سایز {size.name} برابر {size.stock} عدد است.')
    elif action == 'decrease':
        if current_qty - 1 > 0:
            cart.add(product=size.product, size=size, quantity=current_qty - 1, override_quantity=True)
        else:
            cart.remove(size_id)

    return redirect('cart_detail')