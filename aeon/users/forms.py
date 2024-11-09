from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import PasswordInput, TextInput, EmailField
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Ваш пароль', 'id': 'id_password1'})
        self.fields['email'].label = "E-mail"
        self.fields['first_name'].label = "Ім'я"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = 'Підтвердження пароля'

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Ваш e-mail', 'id': 'id_email'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Ваш пароль', 'id': 'id_password1'})
        self.fields['password'].label = "Пароль"
        self.fields['username'].label = "Електронна пошта"

class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, label="Email")
    password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['email', 'first_name']

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Електронна пошта"
        self.fields['first_name'].label = "Ім'я"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', "Паролі не співпадають.")
            elif len(password1) < 8:
                self.add_error('password1', "Пароль повинен містити не менше 8 символів.")

