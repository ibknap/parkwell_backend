from django.http.response import Http404, HttpResponseRedirect
from main.forms import BookingForm, ContactUsForm, NotifyForm
from django.views.generic import TemplateView, DetailView
from django.core.mail import send_mail, BadHeaderError
from parkwell_backend.settings import EMAIL_HOST_USER
from django.shortcuts import redirect, render
from rest_framework.response import Response
from django.views.generic.base import View
from email.errors import HeaderParseError
from django.contrib import messages
from django.template import loader
from company.models import Company
from rest_framework import status
from main.models import Booking
from django.db.models import Q
from park.models import Park
from itertools import chain
import socket

class Main(TemplateView):
    template_name = "main/main.html"
    
class Notify(View):
    def post(self, request, *args, **kwargs):
        notify_form = NotifyForm(request.POST)
        if notify_form.is_valid():
            context = {}
            subject = 'Live Notification'
            name = notify_form.cleaned_data.get('name')
            from_email = notify_form.cleaned_data.get('email')

            context['subject'] = 'Live Notification'
            context['name'] = notify_form.cleaned_data.get('name')
            context['from_email'] = notify_form.cleaned_data.get('email')
            context['message'] = "Live Notification Listing!!!"
            actual_message = loader.render_to_string('emails/message.html', context)
            try:
                send_mail(subject, actual_message, from_email, [EMAIL_HOST_USER,], fail_silently=False, html_message=actual_message)
                messages.success(request, 'Notification for "Live Launch" successfully sent')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except socket.gaierror:
                messages.error(request, 'No internet connect! check your network.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except HeaderParseError:
                messages.error(request, 'A user has an invalid email domain')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except BadHeaderError:
                messages.error(request, 'Bad header')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except TimeoutError:
                messages.error(request, 'Time out')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Booking(View):
    template_name='booking/detail.html'

    def get(self, request, pk, *args, **kwargs):
        context = {}
        park = Park.objects.get(id=pk)
        context['park'] = park
        return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('POST request!')

class BookingDetail(DetailView):
    model = Booking
    template_name='booking/detail.html'
    context_object_name = "booking"

class BookingControl(View):
    def get_object(self, id):
        try:
            return Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            raise Http404

    def post(self, request, park_id, id, *args, **kwargs):
        try:
            park = Park.objects.get(id=park_id)
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking_save = booking_form.save(commit=False)
                booking_save.park = park
                booking_save.save()
                messages.success(request, 'Successfully booked a space!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            messages.error(request, 'Park not associated with parkwell!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def delete(self, request, park_id, id, *args, **kwargs):
        booking = self.get_object(id)
        booking.delete()
        messages.success(request, 'Successfully deleted booking!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ContactUs(View):
    def get(self, request, *args, **kwargs):
        return redirect('main')

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            context = {}
            from_email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            to_email = EMAIL_HOST_USER
            context['name'] =  name
            context['from_email'] =  from_email
            context['subject'] = subject
            context['message'] = message
            actual_message = loader.render_to_string('emails/message.html', context)

            try:
                send_mail(subject, actual_message, from_email, [to_email], fail_silently = False, html_message=actual_message)
                messages.success(request, 'Message sent')
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

class SearchAutocomplete(View):
    def get(self, request, *args, **kwargs):
        query_results = list()
        if 'term' in request.GET:
            query_term = request.GET.get('term')
            search_park = Park.objects.filter(park_name__icontains=query_term)
            search_company = Company.objects.filter(company_name__icontains=query_term)
                                                
            for query in search_park:
                query_results.append(query.park_name)
            for query in search_company:
                query_results.append(query.company_name)

            return Response(query_results)
        return Response({"message": "'term' not in search!"}, status=status.HTTP_400_BAD_REQUEST)

class Search(View):
    model = Park
    template_name = "home/search_page.html"
    def get_queryset(self):
        search_queries = self.request.GET.get('search', '')
        parks = Park.objects.filter(Q(park_name__icontains=search_queries) | Q(park_address__icontains=search_queries))
        companies = Company.objects.filter(Q(company_name__icontains=search_queries))
        search_results = list(chain(parks, companies))
        return search_results
    
    def get(self, request, *args, **kwargs):
        return Response(self.get_queryset())

# handling page errors
def error_400(request, exception):
    return render(request, 'notification/error_pages/400.html', status=400)
def error_403(request, exception):
    return render(request, 'notification/error_pages/403.html', status=403)
def error_404(request, exception):
    return render(request, 'notification/error_pages/404.html', status=404)
def error_500(request):
    return render(request, 'notification/error_pages/500.html', status=500)