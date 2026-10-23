from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import UserProfile, Child

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')

    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('product_list')

@login_required
def profile_view(request):
    orders = request.user.orders.all().order_by('-created')

    return render(request, 'accounts/profile.html', {'orders': orders})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # ذخیره اطلاعات پیش‌فرض جنگو
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        # ذخیره اطلاعات اختصاصی پروفایل
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        return redirect('accounts:profile')
        
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def orders_view(request):
    # استخراج سفارشات پرداخت شده همین کاربر
    orders = Order.objects.filter(user=request.user, paid=True).order_by('-created')
    return render(request, 'accounts/profile_orders.html', {'orders': orders})

@login_required
def children_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        height = request.POST.get('height') or None
        weight = request.POST.get('weight') or None
        chest = request.POST.get('chest') or None
        
        if name and birth_date:
            Child.objects.create(
                user=request.user, 
                name=name, 
                birth_date=birth_date,
                height=height,
                weight=weight,
                chest=chest
            )
        return redirect('accounts:profile_children')
        
    children = request.user.children.all()
    return render(request, 'accounts/profile_children.html', {'children': children})