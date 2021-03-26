import pytest
from project_app.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_register(client):

    assert User.objects.all().count() == 0

    post_data = {
        'email': 'email@onet.pl',
        'first_name': 'Artur',
        'last_name': 'Duda',
        'password': 'Duda_123',
        'password_repeat': 'Duda_123'
    }

    response = client.post(reverse('register'), post_data)
    assert User.objects.all().count() == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_profile(client, user_test, donation):

    client.force_login(user=user_test, backend=None)
    response = client.get(reverse('profile'))
    assert response.status_code == 200
    assert response.context['user'].email == user_test.email
    assert response.context['user'].first_name == user_test.first_name
    assert response.context['user'].last_name == user_test.last_name
    assert response.context['user'].is_superuser is False
    assert response.context['donations'][0].institution == donation.institution
    assert response.context['donations'][0].quantity == donation.quantity
    assert response.context['donations'][0].address == donation.address
    assert response.context['donations'][0].categories == donation.categories
    assert response.context['donations'][0].city == donation.city
    assert response.context['donations'][0].zip_code == donation.zip_code
    assert response.context['donations'][0].phone_number == donation.phone_number
    assert response.context['donations'][0].pick_up_date == donation.pick_up_date
    assert response.context['donations'][0].pick_up_time == donation.pick_up_time
    assert response.context['donations'][0].pick_up_comment == donation.pick_up_comment
