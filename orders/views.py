from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    product_size=item['size']
                )

            cart.clear()

            return render(request, 'orders/order_created.html', {'order': order})
        else:
            # === این دو خط را اضافه کنید تا دلیل ارور را در ترمینال ببینیم ===
            print("❌ ارورهای فرم:")
            print(form.errors)

    else:
        form = OrderCreateForm()


    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

@login_required(login_url='login')
def user_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'orders/order_detail.html', {'order': order})