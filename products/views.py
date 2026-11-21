from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Products, Category, Comment
from django.db.models import Avg, Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import ProductSize, StockNotification
from core.telegram_utils import notify_stock_request

# Create your views here.

def product_list(request):
    products = Products.objects.filter(is_active=True).order_by('-id')
    categories = Category.objects.filter(parent=None)

    user_children = request.user.children.all() if request.user.is_authenticated else None
    selected_child = None
    child_id = request.GET.get('child')

    # فیلتر هوشمند تک‌کلیکی بر اساس مشخصات فرزند
    if request.user.is_authenticated and child_id:
        selected_child = request.user.children.filter(id=child_id).first()
        if selected_child:
            age = max(1, selected_child.get_age())
            products = products.filter(
                gender__in=[selected_child.gender, 'unisex'],
                min_age__lte=age,
                max_age__gte=age,
            )

            # اگر قد ثبت شده باشد، فقط کالاهایی که سایز موجود و متناسب با قد دارند نمایش داده می‌شوند
            if selected_child.height:
                target_height = selected_child.height + (3 if selected_child.body_type == 'chubby' else 0)
                products = products.filter(
                    Q(sizes__stock__gt=0, sizes__min_height__lte=target_height, sizes__max_height__gte=target_height) |
                    Q(sizes__stock__gt=0, sizes__min_height__isnull=True, sizes__max_height__isnull=True)
                ).distinct()

    gender = request.GET.get('gender')
    if not selected_child and gender in ['boy', 'girl']:
        products = products.filter(gender=gender)

    search_query = request.GET.get('q')
    category_id = request.GET.get('category')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        category_ids_list = selected_category.get_all_descendants()
        products = products.filter(category_id__in=category_ids_list)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'products/product_list.html',
        {
            'products': page_obj,
            'categories': categories,
            'current_search': search_query,
            'current_category': category_id,
            'user_children': user_children,
            'selected_child': selected_child,
        }
    )


def product_detail(request, pk):

    product = get_object_or_404(Products, pk=pk)

    children = request.user.children.all() if request.user.is_authenticated else None

    similar_products = Products.objects.filter(gender=product.gender, is_active=True).exclude(id=product.id)[:4]

    comments_list = product.comments.filter(is_active=True)

    paginator = Paginator(comments_list, 10)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    avg_dict = comments_list.aggregate(Avg('rating'))
    avg_rating = round(avg_dict['rating__avg'], 1) if avg_dict['rating__avg'] else 0
    comments_count = comments_list.count()

    if request.method == 'POST':
        auto_name = request.user.get_full_name() or request.user.username
        body = request.POST.get('body')
        rating = request.POST.get('rating')

        if body and rating:
            Comment.objects.create(product=product, name=auto_name, body=body, rating=rating)
            # رفرش کردن صفحه برای جلوگیری از ارسال مجدد فرم
            return redirect('product_detail', pk=product.id)
        
    return render (request, 
                   'products/product_detail.html', 
                   {
                       'product': product,
                       'similar_products': similar_products,
                       'comments': comments,
                       'avg_rating': avg_rating,     
                       'comments_count': comments_count,
                       'children': children,
                    })

@require_POST
def notify_stock(request):
    size_id = request.POST.get('size_id')
    phone = request.POST.get('phone', '').strip()
    size = get_object_or_404(ProductSize, id=size_id)

    if phone:
        _, created = StockNotification.objects.get_or_create(
            size=size,
            phone=phone,
            notified=False,
            defaults={'user': request.user if request.user.is_authenticated else None}
        )
        if created:
            notify_stock_request(size, phone)
        messages.success(request, 'شماره شما ثبت شد. به محض موجود شدن این سایز خبرتان می‌کنیم!')

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))