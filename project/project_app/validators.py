

def validate_password(password):

    if len(password) < 7:
        return ('Hasło za krótkie')

    contains_lower_char = False
    contains_upper_char = False
    for char in password:
        if char.islower():
            contains_lower_char = True
            break
    for char in password:
        if char.isupper():
            contains_upper_char = True
            break
    if (contains_lower_char is False) or (contains_upper_char is False):
        return ('Hasło musi zawierać małe i duże litery')

    if not any([char.isdigit() for char in password]):
        return ('Hasło musi zawierać minimum jedną cyfrę')

    special_char = """!@#$%^&*()_+-={}[]|\:";'<>?,./"""
    contains_special_char = False
    for char in special_char:
        if char in password:
            contains_special_char = True
            break
    if contains_special_char is False:
        return (f'Hasło musi zawierać znak specjalny {special_char}')
