from .models import STATUS_CHOICE


def create_list(institutions):
    data = []
    for institution in institutions:
        data.append({
            'name': f'{STATUS_CHOICE[institution.type][1]}: "{institution.name}"',
            'description': f'Cel i misja: {institution.description}',
            'categories': ', '.join([category.name for category in institution.categories.all()])
        })

    return data
