from django.shortcuts import render
from .models import Category, ProductProxy, Product
from django.views.generic.list import ListView

class IndexView(ListView):
    model = ProductProxy
    template_name = 'shop/index.html'
    context_object_name = 'products'
