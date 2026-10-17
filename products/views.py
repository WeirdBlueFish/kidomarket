from django.shortcuts import render, get_object_or_404
from .models import Products

# Create your views here.

def product_list(request):

    gender_filter = request.GET.get('gender')

    products = Products.objects.filter(is_active=True)

    if gender_filter:
        products = products.filter(gender=gender_filter)

    return render(
        request, 
        'products/product_list.html', 
        {'products': products, 'current_gender': gender_filter}
                  )


def product_detail(request, pk):

    product = get_object_or_404(Products, pk=pk)

    return render (request, 'products/product_detail.html', {'product': product})