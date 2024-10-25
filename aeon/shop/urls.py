from django.urls import path
from .views import ProductDetailView, IndexView, RateView, CategoryListView, WishListView, add_to_wishlist
app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('<slug:category__slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category__slug>/', CategoryListView.as_view(), name='category_list'),
    path('rate/<int:product_id>/<int:rating>/', RateView.as_view()),
]
