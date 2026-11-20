from products.models import Products, ProductSize
from coupens.models import Coupon
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, size, quantity=1, override_quantity=False):
        size_id = str(size.id)

        if size_id not in self.cart:
            self.cart[size_id] = {
                'price': size.price,
                'quantity': 0,
                'product_id': str(product.id)
            }

        if override_quantity:
            self.cart[size_id]['quantity'] = quantity
        else:
            self.cart[size_id]['quantity'] += quantity

        # جلوگیری از ثبت تعداد بیشتر از موجودی انبار
        if self.cart[size_id]['quantity'] > size.stock:
            self.cart[size_id]['quantity'] = size.stock

        # اگر تعداد صفر یا کمتر شد، آیتم از سبد حذف شود
        if self.cart[size_id]['quantity'] <= 0:
            del self.cart[size_id]

        self.session.modified = True

    def remove(self, size_id):
        size_id = str(size_id)
        if size_id in self.cart:
            del self.cart[size_id]
            self.session.modified = True

    def clear(self):
        del self.session['cart']
        if 'coupon_id' in self.session:
            del self.session['coupon_id']
        self.session.modified = True

    def __iter__(self):
        size_ids = self.cart.keys()
        sizes = ProductSize.objects.filter(id__in=size_ids).select_related('product')

        cart = self.cart.copy()
        for size in sizes:
            cart[str(size.id)]['product'] = size.product
            cart[str(size.id)]['size'] = size

        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()