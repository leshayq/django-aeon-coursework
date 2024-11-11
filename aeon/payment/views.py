from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress
from django.http import JsonResponse
@login_required(login_url='/users/login/')
def checkout(request):
    cart = Cart(request)
    cart_items = list(cart) 
    cart_total = cart.get_total_price() 
    title = 'Оформлення замовлення'
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'title': title,
    }

    if request.user.is_authenticated:
        shipping_address, created = ShippingAddress.objects.get_or_create(user=request.user)
        if shipping_address:
            context['shipping_address'] = shipping_address
            return render(request, 'payment/checkout.html', context)


    return render(request, 'payment/checkout.html', context)

@login_required(login_url='/users/login/')
def complete_order(request):
    if request.method == 'POST':
        delivery_type = request.POST.get('delivery_type')
        print(delivery_type)

        match delivery_type:
            case 'Самовивіз':
                print('самовівоз')
                full_name = request.POST.get('name')
                email = request.POST.get('email')
                number = request.POST.get('number')
                address = 'вул. Незалежної України, 43'
                city = None
                department = None
            case "Кур'єр по місту":
                full_name = request.POST.get('name')
                email = request.POST.get('email')
                number = request.POST.get('number')
                address = request.POST.get('address')
                city = request.POST.get('city')
                department = None
            case 'Доставка у відділення':
                full_name = request.POST.get('name')
                email = request.POST.get('email')
                number = request.POST.get('number')
                address = request.POST.get('address')
                city = request.POST.get('city')
                department = request.POST.get('department')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user = request.user,
            defaults={
                'full_name': full_name,
                'email': email,
                'number': number,
                'street_address': address,
                'city': city,
                'department': department,
            }
        )

        shipping_address.full_name = full_name
        shipping_address.email = email
        shipping_address.number = number
        shipping_address.street_address = address
        shipping_address.city = city
        shipping_address.department = department
        shipping_address.save()

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, total=total_price, delivery_type=delivery_type   )

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['qty'], user=request.user)
        else:
            return redirect('users:login')

        
        return JsonResponse({'success': True})
    
@login_required(login_url='/users/login/')
def payment_success(request):
    if 'session_key' in request.session:
        del request.session['session_key']
    return render(request, 'payment/payment_success.html')

@login_required(login_url='/users/login/')
def payment_fail(request):
    return render(request, 'payment/payment_fail.html')