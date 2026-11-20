from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

           
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            # ثبت هزینه ارسال روی سفارش
            order.shipping_cost = int(cart.get_shipping_cost())

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
        initial_data = {}
        if request.user.is_authenticated:
            # ۱. پر کردن پایه از اطلاعات حساب کاربری
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }

            # ۲. اگر پروفایل کاربری فیلد شماره، کد پستی یا آدرس دارد
            profile = getattr(request.user, 'profile', None)
            if profile:
                if getattr(profile, 'phone', None):
                    initial_data['phone'] = profile.phone
                if getattr(profile, 'zip_code', None):
                    initial_data['zip_code'] = profile.zip_code
                if getattr(profile, 'address', None):
                    initial_data['address'] = profile.address

            # ۳. اولویت با آخرین سفارش ثبت‌شده همین کاربر
            last_order = Order.objects.filter(user=request.user).order_by('-id').first()
            if last_order:
                initial_data.update({
                    'first_name': last_order.first_name,
                    'last_name': last_order.last_name,
                    'phone': last_order.phone,
                    'zip_code': last_order.zip_code,
                    'address': last_order.address,
                })

        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


@login_required(login_url='login')
def user_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})