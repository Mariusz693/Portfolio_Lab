from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager

# Create your models here.

STATUS_CHOICE = (
        (0, 'Fundacja'),
        (1, 'Organizacja pozarządowa'),
        (2, 'Zbiórka lokalna')
    )


class User(AbstractUser):

    username = None
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.first_name


class Category(models.Model):

    name = models.CharField(max_length=128, verbose_name='Nazwa')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Institution(models.Model):

    name = models.CharField(max_length=256, verbose_name='Nazwa')
    description = models.TextField(null=True, verbose_name='Opis')
    type = models.SmallIntegerField(choices=STATUS_CHOICE, default=0, verbose_name='Rodzaj')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie darowizn')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instytucja'
        verbose_name_plural = 'Instytucje'


class Donation(models.Model):

    quantity = models.SmallIntegerField(verbose_name='Ilość worków')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie darowizn')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=128, verbose_name='Adres')
    phone_number = models.CharField(max_length=9, verbose_name='Numer telefonu')
    city = models.CharField(max_length=64, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data odbioru')
    pick_up_time = models.TimeField(verbose_name='Godzina odbioru')
    pick_up_comment = models.TextField(blank=True, verbose_name='Uwagi')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='Użytkownik')
    is_taken = models.BooleanField(blank=True, default=False, verbose_name='Odebrano')

    def __str__(self):
        return f'{self.user} {self.pick_up_date}'

    class Meta:
        verbose_name = 'Darowizna'
        verbose_name_plural = 'Darowizny'
