from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Products, Category, Comment
from django.db.models import Avg 
# Create your views here.

def product_list(request):

    products = Products.objects.filter(is_active=True)

    categories = Category.objects.filter(parent=None)


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
            'current_category': category_id
            }
                  )


def product_detail(request, pk):

    product = get_object_or_404(Products, pk=pk)

    similar_products = Products.objects.filter(gender=product.gender, is_active=True).exclude(id=product.id)[:4]

    comments = product.comments.filter(is_active=True)

    avg_dict = comments.aggregate(Avg('rating'))
    avg_rating = round(avg_dict['rating__avg'], 1) if avg_dict['rating__avg'] else 0
    comments_count = comments.count()

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
                       'comments_count': comments_count
                    })