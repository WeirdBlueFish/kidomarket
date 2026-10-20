from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = sum(item.price * item.quantity for item in order.items.all())

    if request.method == 'POST':
        # اگر کاربر روی دکمه "پرداخت موفق" کلیک کرد
        if 'pay' in request.POST:
            order.paid = True
            order.save()
            
            # --- منطق کسر از انبار ---
            # حالا که پرداخت تایید شد، لباس‌ها را از انبار کم می‌کنیم
            for item in order.items.all():
                product_in_db = item.product
                product_in_db.stock -= item.quantity
                
                # اگر موجودی صفر یا منفی شد، لباس ناموجود می‌شود
                if product_in_db.stock <= 0:
                    product_in_db.stock = 0
                    product_in_db.is_active = False 
                    
                product_in_db.save()
            # -------------------------

            return render(request, 'payment/result.html', {'success':True, 'order': order})

        # اگر کاربر روی دکمه "انصراف/پرداخت ناموفق" کلیک کرد
        else:
            return render(request, 'payment/result.html', {'success':False, 'order': order})

    return render(request, 'payment/process.html', {'order': order, 'total_price': total_price})