import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
# from liqpay import LiqPay
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime
from novaposhta.client import NovaPoshtaApi
import dotenv
import os

dotenv.load_dotenv()

client = NovaPoshtaApi(os.getenv('NOVA_POSHTA_API'), timeout=30)

def search_cities(request):
    query = request.GET.get('query', '')
    if query:
        # Получаем данные из API Новой Почты
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
    cart = Cart(request)
    cart_items = list(cart)
    cart_total = cart.get_total_price()

    title = 'Оформлення замовлення'
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'title': title,
    }

    # if request.method == 'POST':
    #     liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    #     params = {
    #         'action': 'pay',
    #         'amount': str(cart_total),
    #         'currency': 'UAH',
    #         'description': 'Оплата замовлення',
    #         'order_id': f'order_{request.user.id}_{cart_total}_{int(datetime.now().timestamp())}',
    #         'version': '3',
    #         'sandbox': 0,  
    #         'server_url': request.build_absolute_uri('/payment/callback/'),
    #         'result_url': request.build_absolute_uri('/payment/payment_success/'),
    #     }
    #     signature = liqpay.cnb_signature(params)
    #     data = liqpay.cnb_data(params)
    #     context.update({'signature': signature, 'data': data})
    #     return render(request, 'payment/pay.html', context)

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

    
@login_required(login_url='/users/login/')
def payment_success(request):
    if 'session_key' in request.session:
        del request.session['session_key']
    return render(request, 'payment/payment_success.html')

@login_required(login_url='/users/login/')
def payment_fail(request):
    return render(request, 'payment/payment_fail.html')


class PayView(TemplateView):
    template_name = 'payment/pay.html'

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '100',
            'currency': 'USD',
            'description': 'Payment for clothes',
            'order_id': 'order_id_1',
            'version': '3',
            'sandbox': 1,
            'server_url': request.build_absolute_uri('/payment/callback/'),
            'result_url': request.build_absolute_uri('/payment/payment_success/'), 
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})

@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        
        if sign == signature:
            print('callback is valid')
            response = liqpay.decode_data_from_str(data)
            print('callback data', response)
            
            if response.get('status') == 'success':
                return redirect('payment:payment_success')
            else:
                return redirect('payment:payment_fail')

        return HttpResponse(status=400)
