from django.urls import path
from . import views

urlpatterns = [
    # مسیر صفحه اصلی پیشخوان آماری
    path('', views.dashboard_home, name='dashboard_home'),
    
    # مسیر صفحه مدیریت (لیست) محصولات
    path('products/', views.dashboard_product_list, name='dashboard_product_list'),
    path('products/add/', views.dashboard_product_add, name='dashboard_product_add'),
    path('products/edit/<int:pk>/', views.dashboard_product_edit, name='dashboard_product_edit'),
    path('products/delete/<int:pk>/', views.dashboard_product_delete, name='dashboard_product_delete'),
    
]