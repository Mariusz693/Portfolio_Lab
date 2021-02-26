from .models import User


def validate_email(email):

    split_email = email.split('@')

    if len(split_email) == 2:
        split_email_domain = split_email[1].split('.')
        if len(split_email_domain) < 2:
            return 'Błąd adresu email'
        elif User.objects.filter(email=email):
            return 'Email już zarejestrowany'
        else:
            return 1
    else:
        return 'Błąd adresu email'