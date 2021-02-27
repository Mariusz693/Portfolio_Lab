from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from .models import Donation, Institution, User
from .validators import validate_email
# Create your views here.


class LandingPageView(View):

    def get(self, request):

        donation_all = Donation.objects.all()
        donation_counter = 0
        for donation in donation_all:
            donation_counter += donation.quantity
        institution_all = Institution.objects.all()
        institution_counter = 0
        for institution in institution_all:
            if institution.donation_set.first() is not None:
                institution_counter += 1

        # foundations = institution_all.filter(type=1).order_by('name')
        foundations = Institution.objects.filter(type=1).order_by('name')
        organizations = Institution.objects.filter(type=2).order_by('name')
        local_collections = Institution.objects.filter(type=3).order_by('name')
        paginator_foundations = Paginator(foundations, 5)
        paginator_foundations_counter = [i + 1 for i in range(paginator_foundations.num_pages)]
        paginator_organizations = Paginator(organizations, 5)
        paginator_organizations_counter = [i + 1 for i in range(paginator_organizations.num_pages)]
        paginator_local_collections = Paginator(local_collections, 5)
        paginator_local_collections_counter = [i + 1 for i in range(paginator_local_collections.num_pages)]
        page = request.GET.get('page')
        institution = request.GET.get('institution')
        if institution and page:
            data = []
            if institution == '1':
                foundations = paginator_foundations.get_page(page)
                for foundation in foundations:
                    data.append({
                        'name': foundation.name,
                        'description': foundation.description,
                        'categories': ', '.join([category.name for category in foundation.categories.all()])
                    })
            elif institution == '2':
                organizations = paginator_organizations.get_page(page)
                for organization in organizations:
                    data.append({
                        'name': organization.name,
                        'description': organization.description,
                        'categories': ', '.join([category.name for category in organization.categories.all()])
                    })
            else:
                local_collections = paginator_local_collections.get_page(page)
                for local_collection in local_collections:
                    data.append({
                        'name': local_collection.name,
                        'description': local_collection.description,
                        'categories': ', '.join([category.name for category in local_collection.categories.all()])
                    })

            return JsonResponse(data, safe=False)

        return render(
            request,
            'index.html',
            context={
                'donation_counter': donation_counter,
                'institution_counter': institution_counter,
                'foundations': paginator_foundations.get_page(page),
                'paginator_foundations_counter': paginator_foundations_counter,
                'organizations': paginator_organizations.get_page(page),
                'paginator_organizations_counter': paginator_organizations_counter,
                'local_collections': paginator_local_collections.get_page(page),
                'paginator_local_collections_counter': paginator_local_collections_counter,
            }
        )


class AddDonationView(View):

    def get(self, request):

        return render(
            request,
            'form.html'
        )


class LoginView(View):

    def get(self, request):

        return render(
            request,
            'login.html'
        )

    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user:
            login(self.request, user)

            return redirect('index')

        else:
            if User.objects.filter(email=email):

                return render(
                    request,
                    'login.html',
                    context={'message': 'Złe hasło'}
                )

            return redirect('register')


class RegisterView(View):

    def get(self, request):

        return render(
            request,
            'register.html'
        )

    def post(self, request):

        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if name == '':
            message = 'Brak imienia'
        elif surname == '':
            message = 'Brak nazwiska'
        elif validate_email(email) != 1:
            message = validate_email(email)
        elif password != password2:
            message = 'Hasła róźnią się od siebie'
        else:
            new_user = User.objects.create_user(
                email=email,
                first_name=name,
                last_name=surname,
                password=password
            )
            return redirect('login')

        return render(
            request,
            'register.html',
            context={'message': message}
        )


class LogoutView(View):

    def get(self, request):

        if self.request.user.is_authenticated:
            logout(request)

        return redirect('index')
