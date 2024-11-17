from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse
from decimal import Decimal

def cart_view(request):
    cart = Cart(request)
    context = {'cart': cart}
    context['title'] = 'Корзина'
    return render(request, 'cart/cart.html', context)

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        product_qty = int(request.POST.get('product_qty'))


        product = get_object_or_404(ProductProxy, id=product_id)

        cart.add(product=product, qty=product_qty)

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, 'product': product.title})

        return response

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})

        return response


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        try:
            product_qty = int(request.POST.get('product_qty'))
        except ValueError:
            product_qty = 1
            
        cart.update(product=product_id, qty=product_qty)

        cart_total = cart.get_total_price()

        # Получаем данные о товаре
        item = cart.cart[str(product_id)]
        item_price = Decimal(item['price'])
        item_total = item_price * item['qty']

        response = JsonResponse({
            'total': cart_total,
            'item_price': item_price,
            'item_qty': item['qty'],
            'item_total': item_total
        })

        return response
