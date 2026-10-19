from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Products

# Create your views here.

def product_list(request):

    products = Products.objects.filter(is_active=True)

    gender_filter = request.GET.get('gender')
    age_filter = request.GET.get('age')
    search_query = request.GET.get('q')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if gender_filter:
        products = products.filter(gender=gender_filter)

    if age_filter and age_filter.isdigit():
        age = int(age_filter)
        products= products.filter(min_age__lte=age, max_age__gte=age)

    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request, 
        'products/product_list.html', 
        {
            'products': page_obj,
            'current_gender': gender_filter, 
            'current_age': age_filter,
            'current_search': search_query
            }
                  )


def product_detail(request, pk):

    product = get_object_or_404(Products, pk=pk)

    return render (request, 'products/product_detail.html', {'product': product})