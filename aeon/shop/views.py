from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, ProductProxy, Product
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class IndexView(ListView):
    model = ProductProxy
    template_name = 'shop/index.html'
    context_object_name = 'index_products'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(available=True)
    
class ProductDetailView(DetailView):
    model = ProductProxy
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return super().get_queryset().filter(slug=self.kwargs['slug'])
    
