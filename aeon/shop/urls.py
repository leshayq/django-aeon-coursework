from django.urls import path
from .views import IndexView, ProductDetailView

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
