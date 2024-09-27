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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductProxy.objects.all()
        for product in products:
            product.rating_count = Rating.objects.filter(product=product).count()
        context['products'] = products
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
