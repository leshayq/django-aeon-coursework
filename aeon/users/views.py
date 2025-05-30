from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from cart.cart import Cart
from payment.models import Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserSettingsForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from payment.models import Order, OrderItem
from .tasks import send_confirming_email

def login_user(request):
    form = UserLoginForm()
    next_url = request.GET.get('next') or request.session.get('next_url') or reverse('shop:main')
    
    if request.GET.get('next'):
        request.session['next_url'] = request.GET.get('next')

    if request.user.is_authenticated:
        return redirect('shop:main')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            
            next_url = request.session.pop('next_url', reverse('shop:main'))
            return HttpResponse(f"<script>window.location.href='{next_url}';</script>")

        else:
            messages.error(request, "Електронна пошта або пароль невірні. Спробуйте ще раз.")
    
    context = {
        'form': form,
    }
    if request.META.get('HTTP_HX_REQUEST'):
        print("HTMX is available")
        return render(request, 'users/auth/login.html', context)

    else:
        print("HTMX is not available")
        return render(request, 'users/auth/login_no_bootstrap.html', context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('shop:main')
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_first_name = form.cleaned_data.get('first_name')
            user_password = form.cleaned_data.get('password1')

            user = CustomUser.objects.create_user(email=user_email, password=user_password, first_name=user_first_name)

            user.is_active = False
            user.save()

            send_confirming_email.delay(user)
            
            return HttpResponse(f"<script>window.location.href='/users/email_verification/';</script>")
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    if request.META.get('HTTP_HX_REQUEST'):
        print("HTMX is available")
        return render(request, 'users/auth/register.html', context)

    else:
        print("HTMX is not available")
        return render(request, 'users/auth/register_no_bootstrap.html', context)

@login_required(login_url='/users/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('shop:main'))

def email_verification(request):
    return render(request, 'users/email/email_verification.html', {'title': 'Підтвердження пошти'})

@login_required(login_url='/users/login/')
def orders_view(request):
    context = {}
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product__images').order_by('-id')
    context['orders'] = orders
    context['title'] = 'Профіль користувача'
    return render(request, 'users/profile/orders.html', context)

@login_required(login_url='/users/login/')
def settings_view(request):
    if request.method == 'POST':
        print('post')
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            print('valid')
            user = form.save(commit=False)
            
            password1 = form.cleaned_data.get("password1")
            if password1:
                user.set_password(password1)
                print('password changed')
                update_session_auth_hash(request, user)
            user.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserSettingsForm(instance=request.user)
    
    return render(request, 'users/profile/settings.html', {'form': form})