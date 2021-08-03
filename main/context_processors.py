from django.core.serializers.json import DjangoJSONEncoder
from account.forms import AdministratorForm, RegisterForm, UpdateFirstNameForm, UpdateLastNameForm
from main.forms import ContactUsForm, WaitlistForm
from django.contrib.auth.models import User
from account.models import Administrator
from company.forms import CompanyForm
from .models import Booking, Waitlist
from company.models import Company
from park.forms import ParkForm
from park.models import Park
import json

def global_context(request):
    context = {}
    context['num_of_parks'] = Park.objects.all().count()
    context['num_of_bookings'] = Booking.objects.all().count()
    context['num_of_users'] = User.objects.all().count()
    context['num_of_admintrators'] = Administrator.objects.all().count()
    context['num_of_companies'] = Company.objects.all().count()

    context['parks'] = Park.objects.order_by("-id")
    context['bookings'] = Booking.objects.order_by("-id")
    context['users'] = User.objects.order_by("-id")
    context['admintrators'] = Administrator.objects.order_by("-id")
    context['cadmins'] = Administrator.objects.filter(is_company_admin=True).order_by("-id")
    context['padmins'] = Administrator.objects.filter(is_park_admin=True).order_by("-id")
    context['companies'] = Company.objects.order_by("-id")
    context['waitlists'] = Waitlist.objects.order_by("-id")

    context['parks_list'] =  json.dumps(list(Park.objects.order_by("-id").values()), cls=DjangoJSONEncoder)
    context['company_list'] = json.dumps(list(Company.objects.order_by("-id").values()), cls=DjangoJSONEncoder)

    context["contact_us_form"] = ContactUsForm()
    context["company_form"] = CompanyForm()
    context["administrator_form"] = AdministratorForm()
    context["register_form"] = RegisterForm()
    context["park_form"] = ParkForm()
    context['waitlist_form'] = WaitlistForm()
    context['update_first_name_form'] = UpdateFirstNameForm()
    context['update_last_name_form'] = UpdateLastNameForm()
    return context