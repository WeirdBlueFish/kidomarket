from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order

# Create your views here.

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    total_price = sum(item.price * item.quantity for item in order.items.all())

    if request.method == 'POST':
        if 'pay' in request.POST:
            order.paid = True
            order.save()
            return render(request, 'payment/result.html', {'success':True, 'order': order})

        else:
            return render(request, 'payment/result.html', {'success':False, 'order': order})

    return render(request, 'payment/process.html', {'order': order, 'total_price': total_price})