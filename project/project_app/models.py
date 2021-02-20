from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    STATUS_CHOICE = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna')
    )
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    type = models.SmallIntegerField(choices=STATUS_CHOICE, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_ip_time = models.TimeField()
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
