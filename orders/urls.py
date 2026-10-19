from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('detail/<int:order_id>/', views.user_order_detail, name='user_order_detail')
]