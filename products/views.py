from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Products, Category

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

    return render (request, 
                   'products/product_detail.html', 
                   {
                       'product': product,
                       'similar_products': similar_products
                    })