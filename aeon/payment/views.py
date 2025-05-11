from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from django.http import JsonResponse
from django.conf import settings
from cart.cart import CartManager
from novaposhta.client import NovaPoshtaApi
import stripe
from django.conf import settings
import dotenv
import os
from django.contrib.auth import get_user_model

User = get_user_model()

dotenv.load_dotenv()

client = NovaPoshtaApi(os.getenv('NOVA_POSHTA_API'), timeout=30)

stripe.api_key = settings.STRIPE_SECRET_KEY

def search_cities(request):
    query = request.GET.get('query', '')
    if query:
        cities = client.address.get_settlements(find_by_string=query, warehouse=1, limit=5)
        return JsonResponse({'success': True, 'data': cities})
    return JsonResponse({'success': False, 'message': 'Query parameter is missing'})

def search_warehouses(request):
    query = request.GET.get('query', '')
    city_name = request.GET.get('city_name', '')
    print(f"Поиск отделений: city_name={city_name}, query={query}")
    
    if city_name and query:
        try:
            warehouses = client.address.get_warehouses(city_name=city_name, warehouse_id=query)
            return JsonResponse({'success': True, 'data': warehouses})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'City name or query parameter is missing'})

@login_required(login_url='/users/login/')
def checkout(request):
    cart = CartManager(request)
    cart_items = cart.get_items()
    cart_total = cart.get_total_price()
    
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'uah',
                'product_data': {
                    'name': item.product.title,
                },
                'unit_amount': int(item.product.price * 100), 
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment:order_success')
        ) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('payment:order_fail')),
        metadata={'user_id': request.user.id}
    )

    title = 'Оформлення замовлення'
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'title': title,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'checkout_session_id': session.id
    }

    return render(request, 'payment/checkout.html', context)

@login_required(login_url='/users/login/')
def complete_order(request):
    if request.method == 'POST':
        cart = CartManager(request)
        cart_items = cart.get_items()

        delivery_type = request.POST.get('delivery_type')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        number = request.POST.get('number')
        city = request.POST.get('city', '')
        street_address = request.POST.get('street_address')
        department = request.POST.get('department', '')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'uah',
                        'product_data': {
                            'name': item.product.title,
                        },
                        'unit_amount': int(item.product.price * 100),
                    },
                    'quantity': item.quantity,
                } for item in cart_items
            ],
            metadata={
                'user_id': request.user.id,
                'full_name': full_name,
                'email': email,
                'number': number,
                'city': city,
                'street_address': street_address,
                'department': department,
                'delivery_type': delivery_type,
                **{f'item_{i}_product_id': str(item.product.id) for i, item in enumerate(cart_items)},
                **{f'item_{i}_quantity': str(item.quantity) for i, item in enumerate(cart_items)},
                'items_count': str(len(cart_items)),
            },
            success_url=request.build_absolute_uri(
                reverse('payment:order_success')
            ) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(
                reverse('payment:order_fail')
            ),
        )

        return JsonResponse({'session_id': session.id, 'stripe_url': session.url})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
def order_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('main:index')

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status != 'paid':
        return redirect('payment:order_fail')

    user = get_object_or_404(User, id=session.metadata['user_id'])

    order = Order.objects.create(
        user=user,
        full_name=session.metadata['full_name'],
        email=session.metadata['email'],
        number=session.metadata['number'],
        city=session.metadata['city'],
        street_address=session.metadata['street_address'],
        department=session.metadata['department'],
        delivery_type=session.metadata['delivery_type'],
        total_price=session.amount_total / 100,
        status='paid'
    )

    from shop.models import Product

    items_count = int(session.metadata.get('items_count', 0))

    for i in range(items_count):
        product_id = session.metadata.get(f'item_{i}_product_id')
        quantity = int(session.metadata.get(f'item_{i}_quantity', 1))
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=quantity
            )
    cart = CartManager(request)
    cart.clear()

    return render(request, 'payment/payment_success.html', {'order': order})


@login_required(login_url='/users/login/')
def order_fail(request):
    return render(request, 'payment/payment_fail.html')
