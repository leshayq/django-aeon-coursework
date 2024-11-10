from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, ProductProxy, Product, Rating, WishList, ImageSlider
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.detail import DetailView
from common.services import all_objects, filter_objects
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .filters import check_filtering
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from users.forms import UserLoginForm
from django.db.models import Q

class IndexView(TemplateView):
    template_name = "shop/index.html"

    def get_products_with_rating(self, items):
        for product in items:
            product.rating_count = Rating.objects.filter(product=product).count()
        return items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductProxy.objects.all().annotate(rating_count=Count('rating')).order_by('-rating_count', 'title')[:20]
        sliding_images = ImageSlider.objects.all().order_by('-created_at')[:8]

        context['products'] = self.get_products_with_rating(products)
        context['sliding_images'] = sliding_images  
        context['title'] = 'AEON| Магазин електронiки'
        return context


class RateView(View, LoginRequiredMixin):
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
        
        product_rating = None
        if self.request.user.is_authenticated:
            product_rating = Rating.objects.filter(product=self.object, user=self.request.user).first()
        self.object.user_rating = product_rating.rating if product_rating else 0
        similars = ProductProxy.objects.exclude(Q(title__contains=self.object)).order_by('-created_at', '-updated_at')[:3]
        context['title'] = self.object.title
        context['rating'] = self.object.user_rating
        context['similars'] = similars

        return context

class CategoryListView(ListView):
    model = ProductProxy
    template_name = 'shop/category_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('category__slug'))
        queryset = super().get_queryset().filter(category=category)

        filters, sort_option = check_filtering(self.request)
        if filters:
            queryset = queryset.filter(**filters)

        if sort_option == 'popularity':
            queryset = queryset.annotate(rating_count=Count('rating')).order_by('-rating_count', 'title')
        elif sort_option:
            queryset = queryset.order_by(sort_option)

        queryset = IndexView.get_products_with_rating(self, queryset)
        return queryset
    def get_context_data(self):
        context = super().get_context_data()
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        category = get_object_or_404(Category, slug=self.kwargs.get('category__slug'))
        
        all_products_in_category = ProductProxy.objects.filter(category=category)

        brand_list = all_products_in_category.values_list('brand', flat=True).distinct().order_by('brand')

        first_brand_list = brand_list[:3]
        remaining_brand_list = brand_list[3:]

        selected_brands = self.request.GET.getlist('brand_key')
        show_all_brands = any(brand in remaining_brand_list for brand in selected_brands)

        context['page_obj'] = page_obj
        context['category_title'] = get_object_or_404(Category, slug=self.kwargs.get('category__slug'))
        context['first_brand_list'] = first_brand_list
        context['remaining_brand_list'] = remaining_brand_list
        context['selected_brands'] = selected_brands
        context['show_all_brands'] = show_all_brands
        
        return context

class WishListView(LoginRequiredMixin, ListView):
    template_name = 'shop/wishlist.html'
    model = WishList
    context_object_name = 'wishlister'

    login_url = '/users/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get("HX-Request"):
                form = UserLoginForm()
                context = {'form': form}
                html = render_to_string('users/login.html', context=context, request=request)
                return HttpResponse(html, content_type="text/html")
            else:
                return redirect(f"{self.login_url}?{self.redirect_field_name}={request.path}")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        raw, created = WishList.objects.get_or_create(user=self.request.user)
        queryset = raw.products.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Список бажань'
        return context


#wishlist actions functions
@login_required(login_url='/users/login/')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(ProductProxy, id=product_id)

    try:
        wishlist = WishList.objects.get(user=request.user)
    except WishList.DoesNotExist:
        wishlist = WishList.objects.create(user=request.user)

    if product in wishlist.products.all():
        return HttpResponse(status=204)

    wishlist.products.add(product)
    return redirect('shop:wishlist')

@login_required(login_url='/users/login/')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(ProductProxy, id=product_id)
    wishlister = WishList.objects.get(user=request.user).products.remove(product)

    return redirect('shop:wishlist')

def search_items(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    
    items = ProductProxy.objects.filter(title__icontains=q)[:7]

    return render(request, 'shop/search_results.html', {'items': items})