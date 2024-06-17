from django.urls import path
from . import views

urlpatterns = [
    path('order_book/', views.order_book_with_addons, name='order_book'),
    path('average_price_set/', views.average_price_set, name='average_price_set'),
]