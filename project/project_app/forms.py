from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import User, Donation
from .validators import validate_email


class UserRegisterForm(forms.Form):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        super(UserRegisterForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise ValidationError('Hasła róźnią się od siebie')

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
                raise ValidationError('Źle podane hasło')

    def authenticate_user(self):

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(email=email, password=password)

        return user


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = '__all__'
