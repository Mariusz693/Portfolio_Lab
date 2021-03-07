from django.shortcuts import render, redirect
from django.views.generic.edit import View, FormView
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from .models import Donation, Institution, User, Category
from .forms import UserRegisterForm, UserLoginForm, DonationForm

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
                        'name': f'Fundacja "{foundation.name}"',
                        'description': f'Cel i misja: {foundation.description}',
                        'categories': ', '.join([category.name for category in foundation.categories.all()])
                    })
            elif institution == '2':
                organizations = paginator_organizations.get_page(page)
                for organization in organizations:
                    data.append({
                        'name': f'Organizacja "{organization.name}"',
                        'description': f'Cel i misja: {organization.description}',
                        'categories': ', '.join([category.name for category in organization.categories.all()])
                    })
            else:
                local_collections = paginator_local_collections.get_page(page)
                for collection in local_collections:
                    data.append({
                        'name': f'Zbiórka "{collection.name}"',
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
        institutions = Institution.objects.all()
        for institution in institutions:
            list_category = []
            for category in institution.categories.all():
                list_category.append(str(category.id))
            institution.category_list = ','.join(list_category)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        return render(
            request,
            'form.html',
            context={'categories': categories, 'institutions': institutions, 'tomorrow': tomorrow}
        )

    def post(self, request):

        data = json.loads(request.body.decode())
        data['user'] = request.user.id
        form = DonationForm(data)

        if form.is_valid():

            form.save()

            return HttpResponse(True)

        return HttpResponse(False)


class LoginView(FormView):

    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):

        if self.request.GET.get('next'):

            return str(self.request.GET.get('next'))

        return '/'

    def form_valid(self, form):

        user = form.authenticate_user()

        if user:
            login(self.request, user)
        else:

            return redirect('register')

        return super(LoginView, self).form_valid(form)


class RegisterView(FormView):

    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = '/login/'

    def form_valid(self, form):

        form.save()

        return super(RegisterView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):

        if self.request.user.is_authenticated:
            logout(request)

        return redirect('index')


class ThanksDonationView(View):

    def get(self, request):

        return render(
            request,
            'form-confirmation.html',
        )
