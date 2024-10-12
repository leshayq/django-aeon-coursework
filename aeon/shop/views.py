from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, ProductProxy, Product, Rating
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.detail import DetailView
from common.services import all_objects, filter_objects
from django.contrib.auth.decorators import login_required
from .filters import check_filtering


# class IndexView(ListView):
#     model = ProductProxy
#     template_name = 'shop/index.html'
#     context_object_name = 'index_products'

#     def get_queryset(self) -> QuerySet[Any]:
#         products = ProductProxy.objects.all()
#         for product in products:
#             rating = Rating.objects.filter(product=product, user=request.user).first()
#             product.user_rating = rating.rating if rating else 0
#         return render(request, "index.html", {"posts": posts})

class IndexView(TemplateView):
    template_name = "shop/index.html"

    def get_products_with_rating(self, items):
        for product in items:
            product.rating_count = Rating.objects.filter(product=product).count()
        return items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductProxy.objects.all()

        context['products'] = self.get_products_with_rating(products)
        return context

# def index(request):
#     products = ProductProxy.objects.all()
#     for product in products:
#         rating = Rating.objects.filter(product=product, user=request.user).first()
#         product.user_rating = rating.rating if rating else 0
#     return render(request, "shop/index.html", {"products": products})

# @login_required()
# def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
#     product = ProductProxy.objects.get(id=product_id)
#     Rating.objects.filter(product=product, user=request.user).delete()
#     product.rating_set.create(user=request.user, rating=rating)
#     return index(request)

class RateView(View):
    def get(self, request, product_id, rating):
        product = ProductProxy.objects.get(id=product_id)
        Rating.objects.filter(product=product, user=request.user).delete()
        product.rating_set.create(user=request.user, rating=rating)
        return redirect('index') 

class ProductDetailView(DetailView):
    model = ProductProxy
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_object(self, *args, **kwargs):
        try:
            return Product.objects.get(slug=self.kwargs.get('slug'), category__slug=self.kwargs.get('category__slug'))
        except Product.DoesNotExists:
            raise Http404
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)    
        context['title'] = self.object.title
        product_rating = None
        if self.request.user.is_authenticated:
            product_rating = Rating.objects.filter(product=self.object, user=self.request.user).first()
        self.object.user_rating = product_rating.rating if product_rating else 0
        context['rating'] = self.object.user_rating

        return context

class CategoryListView(ListView):
    model = ProductProxy
    template_name = 'shop/category_list.html'
    context_object_name = 'category_products'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('category__slug'))
        queryset = super().get_queryset().filter(category=category)

        filters, ordering = check_filtering(self.request)
        if filters:
            queryset = queryset.filter(**filters)

        if ordering:
            queryset = queryset.order_by(ordering)

        queryset = IndexView.get_products_with_rating(self, queryset)
        return queryset
    def get_context_data(self):
        context = super().get_context_data()
        category = get_object_or_404(Category, slug=self.kwargs.get('category__slug'))
        
        all_products_in_category = ProductProxy.objects.filter(category=category)

        brand_list = all_products_in_category.values_list('brand', flat=True).distinct().order_by('brand')

        first_brand_list = brand_list[:3]
        remaining_brand_list = brand_list[3:]

        selected_brands = self.request.GET.getlist('brand_key')
        show_all_brands = any(brand in remaining_brand_list for brand in selected_brands)

        context['category_title'] = get_object_or_404(Category, slug=self.kwargs.get('category__slug'))
        context['first_brand_list'] = first_brand_list
        context['remaining_brand_list'] = remaining_brand_list
        context['selected_brands'] = selected_brands
        context['show_all_brands'] = show_all_brands
        
        return context
    
