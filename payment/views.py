from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = int(order.get_total_cost())

    if request.method == 'POST':
        # اگر کاربر روی دکمه "پرداخت موفق" کلیک کرد
        if 'pay' in request.POST:
            order.paid = True
            order.save()
            
            # --- منطق کسر از انبار ---
            for item in order.items.all():
                if item.product_size:
                    size_in_db = item.product_size
                    size_in_db.stock -= item.quantity

                    if size_in_db.stock <= 0:
                        size_in_db.stock = 0
                    size_in_db.save()
                    
            # -------------------------

            return render(request, 'payment/result.html', {'success':True, 'order': order})

        # اگر کاربر روی دکمه "انصراف/پرداخت ناموفق" کلیک کرد
        else:
            return render(request, 'payment/result.html', {'success':False, 'order': order})

    return render(request, 'payment/process.html', {'order': order, 'total_price': total_price})