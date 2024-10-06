from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


def login_user(request):
    form = UserLoginForm()

    if request.user.is_authenticated:
        return redirect('shop:main')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            print(user.username, user.password)
            return HttpResponse(status=204)
        else:
            messages.error(request, "Ім'я користувача або пароль невірні. Спробуйте ще раз.")
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
            
            return redirect('shop:main')
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form":form})