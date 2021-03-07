from django.core.exceptions import ValidationError

from .models import User


def validate_email(email):

    split_email = email.split('@')

    if len(split_email) == 2:
        split_email_domain = split_email[1].split('.')
        if len(split_email_domain) < 2:
            raise ValidationError('Błąd adresu email')
        if User.objects.filter(email=email):
            raise ValidationError('Email już zarejestrowany')

    else:
        raise ValidationError('Błąd adresu email')
