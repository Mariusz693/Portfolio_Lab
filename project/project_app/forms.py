from django import forms
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator

from .models import User, Donation
from .validators import validate_password


class UserRegisterForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło (min 8 znaków)'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_repeat']

    def clean(self):

        super().clean()
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']

        if validate_password(password):
            self.add_error('password', validate_password(password))

        if password != password_repeat:
            self.add_error('password_repeat', 'Hasła róźnią się od siebie')

    def save(self, commit=True):

        return User.objects.create_user(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password'],
            is_active=False
        )


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

        if validate_password(password_new):
            self.add_error('password_new', validate_password(password_new))

        if password_new != password_repeat:
            self.add_error('password_repeat', 'Nowe hasła róźnią się od siebie')

        if not authenticate(email=email, password=password_check):
            self.add_error('password_check', 'Błędne hasło')


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = [
            'quantity',
            'categories',
            'institution',
            'address',
            'phone_number',
            'city',
            'zip_code',
            'pick_up_date',
            'pick_up_time',
            'pick_up_comment',
            'user',
        ]


class ContactForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())
    email = forms.CharField(widget=forms.EmailInput(), validators=[EmailValidator()])


class UserLoginForm(forms.Form):

    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):

        super().clean()
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        user = User.objects.filter(email=email).first()

        if user:

            if not user.is_active:

                self.add_error('email', 'Twoje konto nie zostało aktywowane, link aktywacyjny otrzymałeś mailem')

            elif not authenticate(email=email, password=password):

                self.add_error('password', 'Błędne hasło')

    def authenticate_user(self):

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(email=email, password=password)

        return user


class ResetPasswordForm(forms.Form):

    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Podaj adres email'}))

    def clean(self):

        super().clean()
        email = self.cleaned_data['email']

        if not User.objects.filter(email=email).first():
            self.add_error('email', 'Brak konta o podanym adresie email')


class SetPasswordForm(forms.Form):

    password_new = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):

        super().clean()
        password_new = self.cleaned_data['password_new']
        password_repeat = self.cleaned_data['password_repeat']

        if validate_password(password_new):
            self.add_error('password_new', validate_password(password_new))

        if password_new != password_repeat:
            self.add_error('password_repeat', 'Nowe hasła róźnią się od siebie')
