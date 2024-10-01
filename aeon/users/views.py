from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['email'])
            # Save the User object
            new_user.save()
            return render(request, 'shop/index.html')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

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
            # messages.success(request, f'Вітаємо {email}!')
            return HttpResponse(status=204)
        else:
            messages.error(request, "Ім'я користувача або пароль невірні. Спробуйте ще раз.")
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)