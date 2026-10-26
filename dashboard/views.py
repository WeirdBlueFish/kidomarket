from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from orders.models import Order, OrderItem
from products.models import Products, ProductImage, ProductSize
from django.contrib.auth.models import User
from django.db.models import Q
from django import forms
import json
import datetime
from django.utils import timezone

@staff_member_required
def dashboard_home(request):
    # دریافت تعداد کل محصولات از کلاسی که تعریف کرده‌اید
    total_products_count = Products.objects.count()
    
    # بعداً می‌توانید سفارشات را فیلتر کنید
    # boy_orders_count = OrderItem.objects.filter(product__gender='boy').count()
    # girl_orders_count = OrderItem.objects.filter(product__gender='girl').count()

    context = {
        'total_products': total_products_count,
        # 'total_income': ...,
        # 'boy_orders': ...,
        # 'girl_orders': ...,
    }
    
    return render(request, 'dashboard/index.html', context)


@staff_member_required
def dashboard_product_list(request):
    query = request.GET.get('q', '')
    
    # دریافت محصولات و اعمال جستجو در صورت وجود کلمه کلیدی
    if query:
        products_list = Products.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by('-id')
    else:
        products_list = Products.objects.all().order_by('-id')
        
    # صفحه‌بندی (نمایش ۱۵ محصول در هر صفحه)
    paginator = Paginator(products_list, 15)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
    }
    return render(request, 'dashboard/product_list.html', context)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'gender', 'min_age', 'max_age', 'image']
        labels = {
            'name': 'نام محصول',
            'description': 'توضیحات کامل',
            'price': 'قیمت پایه (تومان)',
            'gender': 'شعبه / جنسیت',
            'min_age': 'حداقل سن (سال)',
            'max_age': 'حداکثر سن (سال)',
            'image': 'تصویر محصول'
        }

@staff_member_required
def dashboard_product_add(request):
    if request.method == 'POST':
        # از request.FILES برای دریافت تصویر آپلود شده استفاده می‌کنیم
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_product_list')
    else:
        form = ProductForm()
        
    return render(request, 'dashboard/product_form.html', {'form': form})


@staff_member_required
def dashboard_product_edit(request, pk):
    # پیدا کردن محصول یا نمایش ارور ۴۰۴
    product = get_object_or_404(Products, pk=pk)
    
    if request.method == 'POST':
        # آرگومان instance باعث می‌شود اطلاعات قبلی جایگزین شود نه اینکه محصول جدیدی بسازد
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard_product_list')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'dashboard/product_form.html', {'form': form, 'is_edit': True})

@staff_member_required
def dashboard_product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard_product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

# ایمپورت مدل سفارشات (مسیر را بر اساس نام اپلیکیشن سفارشات خود تنظیم کنید)
from orders.models import Order 

@staff_member_required
def dashboard_order_list(request):
    # دریافت تمامی سفارشات، از جدیدترین به قدیمی‌ترین
    orders_list = Order.objects.all().order_by('-created')
    
    # صفحه‌بندی (۱۵ سفارش در هر صفحه)
    paginator = Paginator(orders_list, 15)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/order_list.html', context)


@staff_member_required
def dashboard_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # اگر مدیر وضعیت سفارش را تغییر داد و دکمه ثبت را زد
    if request.method == 'POST':
        new_status = request.POST.get('status')
        # فرض می‌کنیم فیلدی به نام status یا شبیه به آن در مدل Order دارید
        # در غیر این صورت می‌توانید به جای status از فیلدهای موجود خودتان استفاده کنید
        if hasattr(order, 'status'): 
            order.status = new_status
            order.save()
        return redirect('dashboard_order_detail', pk=order.id)
        
    context = {
        'order': order,
    }
    return render(request, 'dashboard/order_detail.html', context)


@staff_member_required
def dashboard_home(request):
    successful_orders = Order.objects.filter(paid=True)
    total_income = sum(order.get_total_cost() for order in successful_orders)
    total_products = Products.objects.count()
    
    boy_orders = OrderItem.objects.filter(order__paid=True, product__gender='boy').count()
    girl_orders = OrderItem.objects.filter(order__paid=True, product__gender='girl').count()
    
    # ۵ سفارش اخیر
    recent_orders = Order.objects.all().order_by('-created')[:5]

    # محاسبه داده‌های نمودار برای ۷ روز گذشته
    today = timezone.now().date()
    persian_weekdays = {0: 'دوشنبه', 1: 'سه‌شنبه', 2: 'چهارشنبه', 3: 'پنجشنبه', 4: 'جمعه', 5: 'شنبه', 6: 'یکشنبه'}
    
    days_labels = []
    girl_sales_data = []
    boy_sales_data = []

    for i in range(6, -1, -1):
        target_day = today - datetime.timedelta(days=i)
        days_labels.append(persian_weekdays[target_day.weekday()])
        
        girl_sales_data.append(OrderItem.objects.filter(
            order__paid=True,
            order__created__date=target_day,
            product__gender='girl'
        ).count())
        
        boy_sales_data.append(OrderItem.objects.filter(
            order__paid=True,
            order__created__date=target_day,
            product__gender='boy'
        ).count())

    context = {
        'total_income': f"{total_income:,}",
        'total_products': total_products,
        'boy_orders': boy_orders,
        'girl_orders': girl_orders,
        'recent_orders': recent_orders,
        # ارسال داده‌ها به صورت JSON برای استفاده در جاوااسکریپت
        'days_labels': json.dumps(days_labels),
        'girl_sales_data': json.dumps(girl_sales_data),
        'boy_sales_data': json.dumps(boy_sales_data),
    }
    return render(request, 'dashboard/index.html', context)


@staff_member_required
def dashboard_user_list(request):
    # دریافت همه کاربران، جدیدترین‌ها در ابتدا
    users_list = User.objects.all().order_by('-date_joined')
    
    # صفحه‌بندی (۱۵ کاربر در هر صفحه)
    paginator = Paginator(users_list, 15)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
    }
    return render(request, 'dashboard/user_list.html', context)


@staff_member_required
def dashboard_product_create(request):
    if request.method == 'POST':
        # ۱. ذخیره محصول اصلی
        product = Products.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            min_age=request.POST.get('min_age') or 0,
            max_age=request.POST.get('max_age') or 0,
            gender=request.POST.get('gender')
        )
        
        # ۲. ذخیره گالری تصاویر
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
            
        # ۳. دریافت و ذخیره سایزها از فرم داینامیک
        size_names = request.POST.getlist('size_name[]')
        size_prices = request.POST.getlist('size_price[]')
        size_stocks = request.POST.getlist('size_stock[]')
        size_min_heights = request.POST.getlist('size_min_height[]')
        size_max_heights = request.POST.getlist('size_max_height[]')
        size_features = request.POST.getlist('size_feature[]')

        for i in range(len(size_names)):
            if size_names[i].strip():  # بررسی خالی نبودن نام سایز
                ProductSize.objects.create(
                    product=product,
                    name=size_names[i],
                    # استفاده از if برای جلوگیری از خطای استرینگ خالی ("")
                    price=size_prices[i] if size_prices[i].strip() else product.price,
                    stock=size_stocks[i] if size_stocks[i].strip() else 0,
                    min_height=size_min_heights[i] if size_min_heights[i].strip() else None,
                    max_height=size_max_heights[i] if size_max_heights[i].strip() else None,
                    features=size_features[i] if i < len(size_features) and size_features[i].strip() else None
                )
            
        return redirect('dashboard_product_list')
        
    return render(request, 'dashboard/product_create.html')