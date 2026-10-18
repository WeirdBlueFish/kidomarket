from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='payment_process')
]