from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
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
