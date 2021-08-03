from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from account.forms import AdministratorForm, LoginForm, RegisterForm, UpdateFirstNameForm, UpdateLastNameForm
from .email_verification_token import email_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from parkwell_backend.settings import EMAIL_HOST_USER
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import DetailView
from rest_framework.generics import GenericAPIView
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from email.errors import HeaderParseError
from account.models import Administrator
from django.views.generic import View
from django.contrib import messages
from django.template import loader
from rest_framework import status
from django.http import Http404
import socket

class UserDetail(DetailView):
    model = User
    template_name='account/user_detail.html'
    context_object_name = "user"

class UserControl(LoginRequiredMixin, View):
    login_url = 'login'
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, id, *args, **kwargs):
        user = self.get_object(id)
        user.delete()
        messages.success(request, 'Successfully deleted user!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Register(View):
    template_name = 'account/register.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already!')
            return redirect('main')
        else:
            self.context['register_form'] = RegisterForm()
            return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            context = {}
            email = register_form.cleaned_data.get('email')
            username = register_form.cleaned_data.get('username')
            register_save = register_form.save(commit=False)
            register_save.is_active = False
            register_save.save()
            current_site = get_current_site(request)
            subject = 'Parkwell Activation.'

            to_email = email
            context['domain'] = current_site.domain
            context['uid'] = urlsafe_base64_encode(force_bytes(register_save.pk))
            context['token'] = email_activation_token.make_token(register_save)
            context['subject'] = subject
            context['message'] = f"Hi {username}, Please verify your parkwell account to be able to login by clicking on the link below to confirm your registration."
            actual_message = loader.render_to_string('emails/message.html', context)

            try:
                send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)
                messages.success(request, 'Check email inbox or spam to confirm email!')
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
        return render(request, self.template_name, {'register_form': register_form})

class VerifyEmail(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
            messages.error(request, 'Invalid user id')
            return redirect('main')
            
        if user is not None and email_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Thank you for your email confirmation. Now you can login.')
            return redirect('login')
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')

class AdminRegister(GenericAPIView):
    template_name = 'account/admin_register.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already!')
            return redirect('main')
        else:
            self.context['register_form'] = RegisterForm()
            self.context['administrator_form'] = AdministratorForm(request.POST)
            return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        administrator_form = AdministratorForm(request.POST, request.FILES)
        if register_form.is_valid() and administrator_form.is_valid():
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            raw_password = register_form.cleaned_data.get('password1')
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
                    user_save.save()
                    administrator_save.save()
                messages.success(request, 'Your account is under verification! Will notify soon.')
                return redirect('admin_login')
        return render(request, self.template_name, {'register_form': register_form, 'administrator_form': administrator_form})

class Login(View):
    template_name = 'account/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already!')
            return redirect('main')
        else:
            self.context['login_form'] = LoginForm()
            return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        authenticate_user = authenticate(username=username, password=password)

        if authenticate_user is not None:
            if authenticate_user.is_active:
                login(request, authenticate_user)
                messages.success(request, f'Welcome { request.user.username }!')
                return redirect('user_detail', pk=request.user.id)
            else:
                messages.info(request, 'Verify your email!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Check user's credentials OR verify your email!!")
            return redirect('login')

class AdminLogin(View):
    template_name = 'account/admin_login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already!')
            return redirect('main')
        else:
            self.context['login_form'] = LoginForm()
            return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        authenticate_user = authenticate(username=username, password=password)

        if authenticate_user is not None:
            if authenticate_user.is_active:
                user = User.objects.get(username=username)
                try:
                    if Administrator.objects.get(user=user, verification=True, is_company_admin=True):
                        login(request, user)
                        messages.success(request, f'{ request.user.username } Login as "Company Admin!"')
                        return redirect('dashboard')
                except Administrator.DoesNotExist:
                    try:
                        if Administrator.objects.get(user=user, verification=True, is_park_admin=True):
                            login(request, user)
                            messages.success(request, f'{ request.user.username } Login as "Park Admin!"')
                            return redirect('dashboard')
                    except Administrator.DoesNotExist:
                        try:
                            is_super_admin = User.objects.get(username=user.username, is_superuser=True)
                            login(request, is_super_admin)
                            messages.success(request, f'{ request.user.username } Login as "Super Admin!"')
                            return redirect('dashboard')
                        except User.DoesNotExist:
                            if Administrator.objects.filter(user=user).exists():
                                messages.error(request, "Administrator not verified!")
                                return redirect('admin_login')
                            messages.error(request, "Check user's credentials!")
                            return redirect('admin_login')
            else:
                messages.info(request, 'Inactive user!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Check user's credentials!")
            return redirect('login')

class Logout(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('main')

class UpdateFirstName(LoginRequiredMixin, View):
    template_name = "account/user_detail.html"
    login_url = 'user_login'

    def post(self, request, *args, **kwargs):
        form = UpdateFirstNameForm(request.POST)
        if form.is_valid():
            change_first_name = form.cleaned_data.get('first_name')
            first_name = User.objects.get(username=request.user)
            first_name.first_name = change_first_name
            first_name.save()
            messages.success(request, "First name Updated!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UpdateLastName(LoginRequiredMixin, View):
    template_name = "account/user_detail.html"
    login_url = 'user_login'

    def post(self, request, *args, **kwargs):
        form = UpdateLastNameForm(request.POST)
        if form.is_valid():
            change_last_name = form.cleaned_data.get('last_name')
            last_name = User.objects.get(username=request.user)
            last_name.last_name = change_last_name
            last_name.save()
            messages.success(request, "Last name Updated!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))