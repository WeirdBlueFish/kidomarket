from products.models import Products

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'price': product.price, 'quantity': 1}
        else:
            self.cart[product_id]['quantity'] +=1

        self.session.modified = True

    def remove(self, product):
        """حذف یک لباس از سبد خرید"""
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def clear(self):
        """پاک کردن کل سبد خرید از حافظه"""
        del self.session['cart']
        self.session.modified = True


    def __iter__(self):
        """گرفتن اطلاعات کامل لباس‌ها از دیتابیس برای نمایش در صفحه"""
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """محاسبه تعداد کل لباس‌های داخل سبد"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """محاسبه قیمت کل سبد خرید"""
        return sum(item['price'] * item['quantity'] for item in self.cart.values())