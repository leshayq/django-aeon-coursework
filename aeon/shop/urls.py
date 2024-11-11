from django.urls import path
from .views import ProductDetailView, IndexView, RateView, CategoryListView, WishListView, add_to_wishlist, remove_from_wishlist, search_items, contact_us_view
app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('search_items', search_items, name='search_items'),
    path('contact_us/', contact_us_view, name='contact_us'), 
    path('<slug:category__slug>/', CategoryListView.as_view(), name='category_list'),
    path('<slug:category__slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('rate/<int:product_id>/<int:rating>/', RateView.as_view()),
]
