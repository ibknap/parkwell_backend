from django.core.mail import send_mail
from main.models import Navigate, Waitlist
from django.views.generic.base import TemplateView
from park.forms import ParkForm
from parkwell_backend.settings import EMAIL_HOST_USER
from account.models import Administrator, ParkAdmin
from django.contrib.auth.models import User
from account.forms import AdministratorForm, ParkAdminForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http.response import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.views.generic import View, DetailView
from django.shortcuts import redirect, render
from company.forms import CompanyForm
from django.contrib import messages
from company.models import Company
from django.utils import timezone
from email.errors import HeaderParseError
from django.template import loader
from park.models import Park
import datetime
import socket
import csv
import random
import string

class DashboardCheckEmail(LoginRequiredMixin, View):
    login_url = 'admin_login'
    
    def post(self, request, email, *args, **kwargs):
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, f'Invalid email! FULL ERROR: {e}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'Valid email!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Dashboard(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name = "dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {}
        try:
            context["company_parks"] = Park.objects.filter(company=request.user.administrator.company)
            context["num_of_company_parks"] = Park.objects.filter(company=request.user.administrator.company).count()
        except:
            context["num_of_company_parks"] = 0
            if request.user.is_superuser:
                return render(request, self.template_name, context)
            messages.error(request, 'No Company Related to account, create one at company section!')
            return render(request, self.template_name, context)
        
        try:
            context["num_of_company_navigate"] = Navigate.objects.filter(company=request.user.administrator.company).count()
            week_ago = timezone.now() - datetime.timedelta(days=7)
            month_ago = timezone.now() - datetime.timedelta(days=30)
            day_100_ago = timezone.now() - datetime.timedelta(days=100)
            
            context["company_navigate_7"] = Navigate.objects.filter(company=request.user.administrator.company, created_on__range=[week_ago, timezone.now()]).count()
            context["company_navigate_30"] = Navigate.objects.filter(company=request.user.administrator.company, created_on__range=[month_ago, timezone.now()]).count()
            context["company_navigate_100"] = Navigate.objects.filter(company=request.user.administrator.company, created_on__range=[day_100_ago, timezone.now()]).count()
        except:
            context["num_of_company_navigate"] = 0
            context["company_navigate_7"] = 0
            context["company_navigate_30"] = 0
            context["company_navigate_100"] = 0
            messages.error(request, 'No navigations done on any parks')
            return render(request, self.template_name, context)
        return render(request, self.template_name, context)

class DashboardCompany(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name = "dashboard/company.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DashboardCompanyDetail(LoginRequiredMixin, DetailView):
    login_url = 'admin_login'
    model = Company
    template_name='dashboard/company_detail.html'

    def get(self, request, pk, *args, **kwargs):
        context = {}
        context['company'] = Company.objects.get(id=pk)
        return render(request, self.template_name, context)

class DashboardCompanyEdit(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/company_edit.html'

    def get(self, request, pk, *args, **kwargs):
        context = {}
        context['company'] = Company.objects.get(id=pk)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        context = {}
        company_form = CompanyForm(request.POST, request.FILES)
        company = Company.objects.get(id=pk)
        context['company'] = company
        context['company_form'] = company_form
        if company_form.is_valid():
            company.company_logo = company_form.cleaned_data.get('company_logo')
            company.company_name = company_form.cleaned_data.get('company_name')
            company.company_email = company_form.cleaned_data.get('company_email')
            company.company_number = company_form.cleaned_data.get('company_number')
            company.company_about = company_form.cleaned_data.get('company_about')
            company.save()
            messages.success(request, 'Company updated!')
            return redirect('dashboard_company_detail', pk=company.id)
        return render(request, self.template_name, context)

class DashboardCompanydAdd(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/company_add.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {}
        company_form = CompanyForm(request.POST, request.FILES)
        context['company_form'] = company_form
        if company_form.is_valid():
            company_save = company_form.save(commit=False)
            company_save.administrator = request.user.administrator
            company_save.verification = True
            company_save.save()
            messages.success(request, 'Company added!')
            return redirect('dashboard_company')
        return render(request, self.template_name, context)

class DashboardCompanyDelete(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request, pk, *args, **kwargs):
        company = Company.objects.get(id=pk)
        company.delete()
        messages.success(request, 'Company deleted!')
        return redirect('dashboard_company')

class DashboardCompanyAdmin(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/account_cadmin.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        administrator_form = AdministratorForm(request.POST, request.FILES)
        if register_form.is_valid() and administrator_form.is_valid():
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Try another")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Try another")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                user_save = register_form.save(commit=False)
                if Administrator.objects.filter(user=user_save).exists():
                    messages.error(request, "User already has a company admin profile. Try another")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    administrator_save = administrator_form.save(commit=False)
                    administrator_save.user = user_save
                    administrator_save.is_company_admin = True
                    administrator_save.verification = True
                    user_save.save()
                    administrator_save.save()
                messages.success(request, 'Company admin added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, self.template_name, {'register_form': register_form, 'administrator_form': administrator_form})

class DashboardCompanyAdminDelete(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request, pk, *args, **kwargs):
        admin = Administrator.objects.get(id=pk)
        user = User.objects.get(id=admin.user.id)
        user.delete()
        messages.success(request, 'Company admin deleted!')
        return redirect('dashboard_cadmin')

class DashboardParkAdmin(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/account_padmin.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        park_admin_form = ParkAdminForm(request.POST, request.FILES)
        if register_form.is_valid() and park_admin_form.is_valid():
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Try another")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Try another")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                user_save = register_form.save(commit=False)
                if ParkAdmin.objects.filter(user=user_save).exists():
                    messages.error(request, "User already has a park admin profile. Try another")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    park_admin_save = park_admin_form.save(commit=False)
                    park_admin_save.user = user_save
                    park_admin_save.company_admin = request.user.administrator
                    user_save.save()
                    park_admin_save.save()
                messages.success(request, 'Park admin added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, self.template_name, {'register_form': register_form, 'park_admin_form': park_admin_form})

class DashboardParkAdminDelete(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request, pk, *args, **kwargs):
        admin = ParkAdmin.objects.get(id=pk)
        user = User.objects.get(id=admin.user.id)
        user.delete()
        messages.success(request, 'Park admin deleted!')
        return redirect('dashboard_padmin')

class DashboardBookings(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/account_booking.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DashboardPark(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name = "dashboard/park.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DashboardParkDetail(LoginRequiredMixin, DetailView):
    login_url = 'admin_login'
    model = Park
    template_name='dashboard/park_detail.html'

    def get(self, request, pk, *args, **kwargs):
        context = {}
        context['park'] = Park.objects.get(id=pk)
        return render(request, self.template_name, context)

class DashboardParkEdit(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/park_edit.html'

    def get_form_kwargs(self):
        kwargs = super(DashboardParkdAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, pk, *args, **kwargs):
        context = {}
        context['park'] = Park.objects.get(id=pk)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        context = {}
        park = Park.objects.get(id=pk)
        park_initial = {}
        park_initial['park_admin'] = park.park_admin
        park_initial['park_name'] = park.park_name
        park_initial['park_email'] = park.park_email
        park_initial['total_parking_space'] = park.total_parking_space
        park_initial['park_number'] = park.park_number
        park_initial['park_address'] = park.park_address
        park_initial['park_lon'] = park.park_lon
        park_initial['park_lat'] = park.park_lat
        park_initial['park_about'] = park.park_about

        park_form = ParkForm(request.POST, request.FILES, request=request, instance=park, initial=park_initial)
        park = Park.objects.get(id=pk)
        context['park'] = park
        context['park_form'] = park_form
        if park_form.is_valid():
            park.park_name = park_form.cleaned_data.get('park_name')
            park.park_email = park_form.cleaned_data.get('park_email')
            park.total_parking_space = park_form.cleaned_data.get('total_parking_space')
            park.park_number = park_form.cleaned_data.get('park_number')
            park.park_address = park_form.cleaned_data.get('park_address')
            park.park_lon = park_form.cleaned_data.get('park_lon')
            park.park_lat = park_form.cleaned_data.get('park_lat')
            park.park_about = park_form.cleaned_data.get('park_about')
            park.save()
            messages.success(request, 'Park updated!')
            return redirect('dashboard_park_detail', pk=park.id)
        return render(request, self.template_name, context)

class DashboardParkdAdd(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/park_add.html'
    form_class = ParkForm

    def get_form_kwargs(self):
        kwargs = super(DashboardParkdAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {}
        park_form = ParkForm(request.POST, request.FILES, request=request)
        context['park_form'] = park_form
        if park_form.is_valid():
            try:
                company = Company.objects.get(administrator=request.user.administrator)
                park_save = park_form.save(commit=False)
                park_save.company = company
                park_save.save()
                messages.success(request, 'Park added!')
                return redirect('dashboard_park')
            except Company.DoesNotExist:
                messages.error(request, 'You are not company admin!')
                return redirect('dashboard_park')
        return render(request, self.template_name, context)

class DashboardParkDelete(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request, pk, *args, **kwargs):
        park = Park.objects.get(id=pk)
        park.delete()
        messages.success(request, 'Park deleted!')
        return redirect('dashboard_park')

class DashboardUsersInfo(LoginRequiredMixin, TemplateView):
    login_url = 'admin_login'
    template_name='dashboard/users_info.html'

class DashboardUsersInfoDelete(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(id=pk)
        user.delete()
        messages.success(request, 'User deleted!')
        return redirect('dashboard_users_info')

class VerifyAdmin(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request, pk, *args, **kwargs):
        context = {}
        admin = Administrator.objects.get(id=pk)
        admin.verification = True
        admin.save()

        context['subject'] = "Company Admin Verified!"
        context['message'] = f"Hi {admin.user.username}, your Parkwell Africa company admin account has been verified! You can how login in and create company and parks."
        actual_message = loader.render_to_string('emails/message.html', context)

        try:
            send_mail("Company Admin Verified! Parkwell.", actual_message, EMAIL_HOST_USER, [admin.user.email], fail_silently = False, html_message=actual_message)
            messages.success(request, 'Company Admin verified!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except socket.gaierror:
            messages.error(request, 'No internet connect')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except HeaderParseError:
            messages.error(request, 'A user has an invalid domain')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except BadHeaderError:
            messages.error(request, 'Bad header')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except TimeoutError:
            messages.error(request, 'Time out')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except ValueError as e:
            messages.error(request, f'{e}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class DashboardWaitlist(View):
    template_name='dashboard/waitlist.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def export_waitlist(request):
    if request.user.is_superuser:
        random_id = f"_{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        waitlist = Waitlist.objects.all()
        response = HttpResponse()
        response['Content-Disposition'] = f'attachment; filename=waitlist{random_id}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'EMAIL ADDRESS'])
        waitlists = waitlist.values_list('id', 'email')
        for wait in waitlists:
            writer.writerow(wait)
        return response
    messages.error(request, "You don't have permission!")
    return redirect('dashboard_waitlist')

def export_verified_company_admin(request):
    if request.user.is_superuser:
        random_id = f"_{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        verified_company_admin = Administrator.objects.filter(is_company_admin=True, verification=True)
        response = HttpResponse()
        response['Content-Disposition'] = f'attachment; filename=verified_company_admin{random_id}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'USERNAME', 'EMAIL ADDRESS', 'PHONE NUMBER'])
        company_admin = verified_company_admin.values_list('id', 'user__username', 'user__email', 'mobile_number')
        for admin in company_admin:
            writer.writerow(admin)
        return response
    messages.error(request, "You don't have permission!")
    return redirect('dashboard_cadmin')

def export_non_verified_company_admin(request):
    if request.user.is_superuser:
        random_id = f"_{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        non_verified_company_admin = Administrator.objects.filter(is_company_admin=True, verification=False)
        response = HttpResponse()
        response['Content-Disposition'] = f'attachment; filename=non_verified_company_admin{random_id}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'USERNAME', 'EMAIL ADDRESS', 'PHONE NUMBER'])
        company_admin = non_verified_company_admin.values_list('id', 'user__username', 'user__email', 'mobile_number')
        for admin in company_admin:
            writer.writerow(admin)
        return response
    messages.error(request, "You don't have permission!")
    return redirect('dashboard_cadmin')

def export_park_admin(request):
    if request.user.is_superuser:
        random_id = f"_{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        park_admin = ParkAdmin.objects.all()
        response = HttpResponse()
        response['Content-Disposition'] = f'attachment; filename=park_admin{random_id}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'USERNAME', 'EMAIL ADDRESS', 'COMPANY ADMIN', 'PHONE NUMBER'])
        park_admins = park_admin.values_list('id', 'user__username', 'user__email', 'company_admin__user__username', 'mobile_number')
        for admin in park_admins:
            writer.writerow(admin)
        return response
    messages.error(request, "You don't have permission!")
    return redirect('dashboard_padmin')

def export_all_users(request):
    if request.user.is_superuser:
        random_id = f"_{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        users = User.objects.all()
        response = HttpResponse()
        response['Content-Disposition'] = f'attachment; filename=users{random_id}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'USERNAME', 'EMAIL ADDRESS', 'FIRST NAME', 'LAST NAME'])
        all_users = users.values_list('id', 'username', 'email', 'first_name', 'last_name')
        for user in all_users:
            writer.writerow(user)
        return response
    messages.error(request, "You don't have permission!")
    return redirect('dashboard_users_info')