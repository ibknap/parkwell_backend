import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from account.forms import AdministratorForm, ParkAdminForm, RegisterForm, UpdateFirstNameForm, UpdateLastNameForm
from main.forms import ContactUsForm, WaitlistForm
from django.contrib.auth.models import User
from account.models import Administrator, ParkAdmin
from company.forms import CompanyForm
from .models import Booking, Navigate, Waitlist
from company.models import Company
from park.forms import ParkForm
from park.models import Park
import json

def global_context(request):
    context = {}
    week_ago = timezone.now() - datetime.timedelta(days=7)
    month_ago = timezone.now() - datetime.timedelta(days=30)
    day_100_ago = timezone.now() - datetime.timedelta(days=100)

    context['num_of_parks'] = Park.objects.all().count()
    context['num_of_bookings'] = Booking.objects.all().count()
    context['num_of_users'] = User.objects.all().count()
    context['num_of_admintrators'] = Administrator.objects.all().count()
    context['num_of_companies'] = Company.objects.all().count()
    context['num_of_navigations'] = Navigate.objects.all().count()
    context["navigate_7"] = Navigate.objects.filter(created_on__range=[week_ago, timezone.now()]).count()
    context["navigate_30"] = Navigate.objects.filter(created_on__range=[month_ago, timezone.now()]).count()
    context["navigate_100"] = Navigate.objects.filter(created_on__range=[day_100_ago, timezone.now()]).count()

    context['parks'] = Park.objects.order_by("-id")
    context['bookings'] = Booking.objects.order_by("-id")
    context['users'] = User.objects.order_by("-id")
    context['admintrators'] = Administrator.objects.order_by("-id")
    context['cadmins'] = Administrator.objects.filter(is_company_admin=True).order_by("-id")
    context['padmins'] = ParkAdmin.objects.order_by("-id")
    context['companies'] = Company.objects.order_by("-id")
    context['waitlists'] = Waitlist.objects.order_by("-id")

    context['parks_list'] =  json.dumps(list(Park.objects.order_by("-id").values()), cls=DjangoJSONEncoder)
    context['company_list'] = json.dumps(list(Company.objects.order_by("-id").values()), cls=DjangoJSONEncoder)

    context["contact_us_form"] = ContactUsForm()
    context["company_form"] = CompanyForm()
    context["administrator_form"] = AdministratorForm()
    context["park_admin_form"] = ParkAdminForm()
    context["register_form"] = RegisterForm()
    context["park_form"] = ParkForm(request=request)
    context['waitlist_form'] = WaitlistForm()
    context['update_first_name_form'] = UpdateFirstNameForm()
    context['update_last_name_form'] = UpdateLastNameForm()
    return context