from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import PasswordInput, TextInput, EmailField

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Ваш e-mail', 'id': 'id_email'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Ваш пароль', 'id': 'id_password1'})
        self.fields['username'].label = "Email"