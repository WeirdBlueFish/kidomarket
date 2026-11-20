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
    path('orders/', views.dashboard_order_list, name='dashboard_order_list'),
    path('orders/<int:pk>/', views.dashboard_order_detail, name='dashboard_order_detail'),
    path('users/', views.dashboard_user_list, name='dashboard_user_list'),
    path('dashboard_product_create/', views.dashboard_product_create, name='dashboard_product_create'),
    path('coupons/', views.dashboard_coupon_list, name='dashboard_coupon_list'),
    path('coupons/add/', views.dashboard_coupon_create, name='dashboard_coupon_create'),
    path('coupons/edit/<int:coupon_id>/', views.dashboard_coupon_edit, name='dashboard_coupon_edit'),
    path('coupons/delete/<int:coupon_id>/', views.dashboard_coupon_delete, name='dashboard_coupon_delete'),
    path('notifications/', views.dashboard_notification_list, name='dashboard_notification_list'),
    path('notifications/<int:pk>/toggle/', views.dashboard_notification_toggle, name='dashboard_notification_toggle'),
    path('shipping/', views.dashboard_shipping_settings, name='dashboard_shipping_settings'),
]