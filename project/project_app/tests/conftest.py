import pytest
import datetime
from django.test import Client
from project_app.models import Category, Institution, User, Donation


@pytest.fixture
def client():
    client = Client()

    return client


@pytest.fixture
def category_toys():
    category = Category.objects.create(
        name='Zabawki'
    )

    return category


@pytest.fixture
def category_clothes():
    category = Category.objects.create(
        name='Ubrania'
    )

    return category


@pytest.fixture
def institution():
    institution = Institution.objects.create(
        name='Fundacja',
        type=1,
        description='Fundacja pomocna'
    )

    return institution


@pytest.fixture
def user_test():
    user = User.objects.create_user(
        first_name='AAAA',
        last_name='BBBB',
        email='ab@onet.pl'
    )

    return user


@pytest.fixture
def donation(institution, user_test, category_toys, category_clothes):
    donation = Donation.objects.create(
        quantity=1,
        institution=institution,
        address='Polna 9',
        phone_number='764323686',
        city='Krk',
        zip_code='67-356',
        pick_up_date=datetime.date(day=25, year=2021, month=3),
        pick_up_time=datetime.time(hour=12, minute=0),
        user=user_test
    )
    donation.categories.set([category_clothes, category_toys])

    return donation


