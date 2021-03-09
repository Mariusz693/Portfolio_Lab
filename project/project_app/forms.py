from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import User, Donation


class UserRegisterForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_repeat']

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']

        if password != password_repeat:
            self.add_error('password', 'Hasła róźnią się od siebie')

    def save(self, commit=True):
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password']
        )


class UserLoginForm(forms.Form):

    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        super(UserLoginForm, self).clean()
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        if User.objects.filter(email=email):
            if not authenticate(email=email, password=password):
                self.add_error('password', 'Błędne hasło')

    def authenticate_user(self):

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(email=email, password=password)

        return user


class UserUpdateForm(forms.Form):

    password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasłem'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        super().clean()
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if not authenticate(email=email, password=password_check):
            self.add_error('password_check', 'Błędne hasło')


class UserPasswordForm(forms.Form):

    password_new = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Poprzednie hasło'}))
    email = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        super().clean()
        password_new = self.cleaned_data['password_new']
        password_repeat = self.cleaned_data['password_repeat']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if password_new != password_repeat:
            self.add_error('password_new', 'Nowe hasła róźnią się od siebie')

        if not authenticate(email=email, password=password_check):
            self.add_error('password_check', 'Błędne hasło')


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = '__all__'
