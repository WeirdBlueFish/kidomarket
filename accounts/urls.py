from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/orders/', views.orders_view, name='profile_orders'),
    path('profile/orders/<int:order_id>/', views.order_detail_view, name='profile_order_detail'),
    path('profile/children/', views.children_view, name='profile_children'),
    path('profile/children/edit/<int:child_id>/', views.child_edit_view, name='child_edit'),
]