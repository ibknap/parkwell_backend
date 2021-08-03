from django.views.generic.base import TemplateView
from park.forms import ParkForm
from account.models import Administrator
from django.contrib.auth.models import User
from account.forms import AdministratorForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http.response import HttpResponseRedirect
from django.views.generic import View, DetailView
from django.shortcuts import redirect, render
from company.forms import CompanyForm
from django.contrib import messages
from company.models import Company
from park.models import Park

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
        return render(request, self.template_name)

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

class DashboardParkAdmin(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/account_padmin.html'

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
                    administrator_save.is_park_admin = True
                    administrator_save.verification = True
                    user_save.save()
                    administrator_save.save()
                messages.success(request, 'Company admin added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, self.template_name, {'register_form': register_form, 'administrator_form': administrator_form})

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

    def get(self, request, pk, *args, **kwargs):
        context = {}
        context['park'] = Park.objects.get(id=pk)
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        context = {}
        park_form = ParkForm(request.POST, request.FILES)
        park = Park.objects.get(id=pk)
        context['park'] = park
        context['park_form'] = park_form
        if park_form.is_valid():
            park.park_name = park_form.cleaned_data.get('park_name')
            park.park_email = park_form.cleaned_data.get('park_email')
            park.total_parking_space = park_form.cleaned_data.get('total_parking_space')
            park.occupied_space = park_form.cleaned_data.get('occupied_space')
            park.park_number = park_form.cleaned_data.get('park_number')
            park.park_address = park_form.cleaned_data.get('park_address')
            park.park_coordinates = park_form.cleaned_data.get('park_coordinates')
            park.park_about = park_form.cleaned_data.get('park_about')
            park.save()
            messages.success(request, 'Park updated!')
            return redirect('dashboard_park_detail', pk=park.id)
        return render(request, self.template_name, context)

class DashboardParkdAdd(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name='dashboard/park_add.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {}
        park_form = ParkForm(request.POST, request.FILES)
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
        admin = Administrator.objects.get(id=pk)
        admin.verification = True
        admin.save()
        messages.success(request, 'Company Admin verified!')
        return redirect('dashboard_cadmin')