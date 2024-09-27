from django.urls import path
from .views import ProductDetailView, IndexView, RateView
app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('<slug:category__slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('rate/<int:product_id>/<int:rating>/', RateView.as_view()),
]
