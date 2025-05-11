from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse
from decimal import Decimal
from .models import Cart, CartItem
from .cart import CartManager
from django.views.decorators.http import require_POST
from shop.models import Product
from django.shortcuts import redirect

def cart_view(request):
    cart = CartManager(request)
    return render(request, 'cart/cart.html', {
        'title': 'Корзина',
        'cart': cart,
        'cart_items': cart.get_items(),
        'total_price': cart.get_total_price()
    })

@require_POST
def cart_add(request, product_id):
    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    update = request.POST.get('update', False) == 'true'
    
    cart.add(product=product, quantity=quantity, update_quantity=update)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_total': cart.get_total_items(),
            'cart_price': cart.get_total_price()
        })
    
    return redirect('cart:cart_view')

@require_POST
def cart_remove(request, product_id):
    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_total': cart.get_total_items(),
            'cart_price': cart.get_total_price()
        })
    
    return redirect('cart:cart_view')

def cart_update(request, product_id):
    if request.method == 'POST':
        cart = CartManager(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity, update_quantity=True)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart_item = CartItem.objects.get(cart=cart.cart, product=product)
            return JsonResponse({
                'status': 'success',
                'item_price': cart_item.get_cost(),
                'cart_total': cart.get_total_items(),
                'cart_price': cart.get_total_price()
            })
        
        return redirect('cart:cart_view')
    
    return redirect('cart:cart_view')