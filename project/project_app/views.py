import datetime
import json

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import View, FormView
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse

from .models import Donation, Institution, Category, STATUS_CHOICE, User, UserUniqueToken
from .forms import UserRegisterForm, UserLoginForm, DonationForm, UserUpdateForm, UserPasswordForm, ContactForm

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

        foundations = Institution.objects.filter(type=0).order_by('name')
        organizations = Institution.objects.filter(type=1).order_by('name')
        local_collections = Institution.objects.filter(type=2).order_by('name')
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
            if institution == '0':
                foundations = paginator_foundations.get_page(page)
                for foundation in foundations:
                    data.append({
                        'name': f'{STATUS_CHOICE[foundation.type][1]}: "{foundation.name}"',
                        'description': f'Cel i misja: {foundation.description}',
                        'categories': ', '.join([category.name for category in foundation.categories.all()])
                    })
            elif institution == '1':
                organizations = paginator_organizations.get_page(page)
                for organization in organizations:
                    data.append({
                        'name': f'{STATUS_CHOICE[organization.type][1]}: "{organization.name}"',
                        'description': f'Cel i misja: {organization.description}',
                        'categories': ', '.join([category.name for category in organization.categories.all()])
                    })
            else:
                local_collections = paginator_local_collections.get_page(page)
                for collection in local_collections:
                    data.append({
                        'name': f'{STATUS_CHOICE[collection.type][1]}: "{collection.name}"',
                        'description': f'Cel i misja: {collection.description}',
                        'categories': ', '.join([category.name for category in collection.categories.all()])
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


@method_decorator(csrf_exempt, name='dispatch')
class AddDonationView(LoginRequiredMixin, View):

    def get(self, request):

        categories = Category.objects.all()
        categories_check = request.GET.get('categories')
        if categories_check:
            institutions = Institution.objects.all().order_by('type')
            categories_check = categories_check.split(',')
            for category in categories_check:
                institutions = institutions.filter(categories=category)
            data = []
            for institution in institutions:
                data.append({
                    'name': f'{STATUS_CHOICE[institution.type][1]} "{institution.name}"',
                    'description': f'Cel i misja: {institution.description}',
                    'id': f'{institution.id}'
                })

            return JsonResponse(data, safe=False)

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        return render(
            request,
            'form.html',
            context={'categories': categories, 'tomorrow': tomorrow}
        )

    def post(self, request):

        data = json.loads(request.body.decode())
        data['user'] = request.user.id
        form = DonationForm(data)

        if form.is_valid():

            form.save()

            return HttpResponse(f'{reverse("confirmation")}?message=1')

        return HttpResponse(f'{reverse("confirmation")}?message=0')


class UserLoginView(FormView):

    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):

        if self.request.GET.get('next'):

            return str(self.request.GET.get('next'))

        return reverse_lazy('index')

    def get_initial(self):

        initial = super().get_initial()
        initial['token'] = self.request.GET.get('token')

        return initial

    def form_valid(self, form):

        user = form.authenticate_user()

        if user:

            login(self.request, user)

        else:

            return redirect('register')

        return super().form_valid(form)


class UserRegisterView(FormView):

    form_class = UserRegisterForm
    template_name = 'register.html'

    def get_success_url(self):

        return f'{reverse("confirmation")}?message=4'

    def form_valid(self, form):

        user = form.save()
        new_token = UserUniqueToken.objects.create(user=user)

        send_mail(
            subject='Rejestracja konta',
            message=f'''Dziękujemy za rejestrację konta w naszym serwisie, twój link do aktywacji konta:
                {self.request.get_host()}{reverse("login")}?token={new_token.token}''',
            from_email='webmaster@localhost',
            recipient_list=[form.cleaned_data['email']],
        )

        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, View):

    def get(self, request):

        form = UserUpdateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })

        return render(
            request,
            'update.html',
            context={'form': form}
        )

    def post(self, request):

        form = UserUpdateForm(request.POST)

        if form.is_valid():

            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            return redirect('index')

        return render(
            request,
            'update.html',
            context={'form': form}
        )


class UserPasswordView(LoginRequiredMixin, View):

    def get(self, request):

        form = UserPasswordForm(initial={
            'email': request.user.email
        })

        return render(
            request,
            'password.html',
            context={'form': form}
        )

    def post(self, request):

        form = UserPasswordForm(request.POST)

        if form.is_valid():

            user = request.user
            user.set_password(form.cleaned_data['password_new'])
            user.save()

            return redirect('login')

        return render(
            request,
            'password.html',
            context={'form': form}
        )


class UserLogoutView(View):

    def get(self, request):

        if self.request.user.is_authenticated:
            logout(request)

        return redirect('index')


class ConfirmationView(View):

    def get(self, request):

        message = request.GET.get('message')

        return render(
            request,
            'form-confirmation.html',
            context={'message': message}
        )


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request):

        user = request.user
        donations = Donation.objects.filter(user=user).order_by('is_taken')
        DonationFormSet = modelformset_factory(Donation, fields=('is_taken',), extra=0)
        formset = DonationFormSet(queryset=donations.filter(is_taken=False))

        return render(
            request,
            'profile.html',
            context={'user': user, 'donations': donations, 'formset': formset}
        )

    def post(self, request):

        DonationFormSet = modelformset_factory(Donation, fields=('is_taken',), extra=0)
        formset = DonationFormSet(request.POST)
        formset.save()

        return redirect('profile')


class ContactView(View):

    def post(self, request):

        form = ContactForm(request.POST)

        if form.is_valid():

            users = User.objects.filter(is_superuser=True).values_list('email')
            users_to_send = [user[0] for user in users]
            send_mail(
                subject=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=users_to_send,
            )

            return redirect(f'{reverse("confirmation")}?message=2')

        return redirect(f'{reverse("confirmation")}?message=3')
