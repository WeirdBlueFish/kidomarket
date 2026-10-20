from products.models import Products, ProductSize # حتما ProductSize را ایمپورت کنید

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    # تابع add حالا سایز را هم به عنوان ورودی می‌گیرد
    def add(self, product, size):
        
        size_id = str(size.id)

        if size_id not in self.cart:
            self.cart[size_id] = {
                'price': size.price, 
                'quantity': 1,
                'product_id': str(product.id)
            }
        else:
            self.cart[size_id]['quantity'] += 1

        self.session.modified = True

    # برای حذف، فقط به آیدی سایز نیاز داریم
    def remove(self, size_id):
        size_id = str(size_id)
        if size_id in self.cart:
            del self.cart[size_id]
            self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.session.modified = True

    def __iter__(self):
        # استخراج تمام آیدیِ سایزهای داخل سبد
        size_ids = self.cart.keys()
        
        # نکته کلیدی: اینجا باید نام فیلد نوشته شود (product) نه نام کلاس (Products)
        sizes = ProductSize.objects.filter(id__in=size_ids).select_related('product')

        cart = self.cart.copy()
        for size in sizes:
            # هم خود لباس و هم سایزش را به دیکشنری اضافه می‌کنیم تا در HTML استفاده کنیم
            cart[str(size.id)]['product'] = size.product
            cart[str(size.id)]['size'] = size

        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())