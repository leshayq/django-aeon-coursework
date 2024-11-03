from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django_email_verification import send_email

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
    return render(request, 'users/login.html', context)


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
            send_email(user)
            
            return HttpResponse(f"<script>window.location.href='/users/email_verification/';</script>")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form":form})

def email_verification(request):
    return render(request, 'users/email/email_verification.html')