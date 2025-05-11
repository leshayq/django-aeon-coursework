from . import views
from django.urls import path

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('complete-order/', views.complete_order, name='complete_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-fail/', views.order_fail, name='order_fail'),

    path('api/search/cities/', views.search_cities, name='search_cities'),
    path('api/search/warehouses/', views.search_warehouses, name='search_warehouses'),
]