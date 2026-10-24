from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from products.models import Products # ایمپورت کلاس محصولات شما
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms

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