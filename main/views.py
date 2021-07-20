from main.serializers import BookingSerializer, ContactUsSerializer
from parkwell_backend.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import TemplateView
from rest_framework.response import Response
from django.views.generic.base import View
from email.errors import HeaderParseError
from rest_framework.views import APIView
from django.http.response import Http404
from django.contrib import messages
from django.shortcuts import render
from django.template import loader
from company.models import Company
from main.forms import NotifyForm
from rest_framework import status
from main.models import Booking
from django.db.models import Q
from park.models import Park
from itertools import chain
import socket

class Main(TemplateView):
    template_name = "main/main.html"

class Docs(TemplateView):
    template_name = "main/docs.html"
    
class Notify(View):
    def post(self, request, format=None):
        notify_form = NotifyForm(request.POST)
        if notify_form.is_valid():
            context = {}
            subject = 'Live Notification'
            name = notify_form.cleaned_data.get('name')
            from_email = notify_form.cleaned_data.get('email')

            context['subject'] = 'Live Notification'
            context['name'] = notify_form.cleaned_data.get('name')
            context['from_email'] = notify_form.cleaned_data.get('email')
            context['message'] = f"Name: {name} \n\n Email: {from_email}"
            actual_message = loader.render_to_string('emails/message.html', context)
            try:
                send_mail(subject, actual_message, from_email, [EMAIL_HOST_USER,], fail_silently=False, html_message=actual_message)
                messages.success(request, 'Notification for "Live Launch" successfully sent')
                return render(request, 'main/message.html')
            except socket.gaierror:
                messages.error(request, 'No internet connect! check your network.')
                return render(request, 'main/message.html')
            except HeaderParseError:
                messages.error(request, 'A user has an invalid email domain')
                return render(request, 'main/message.html')
            except BadHeaderError:
                messages.error(request, 'Bad header')
                return render(request, 'main/message.html')
            except TimeoutError:
                messages.error(request, 'Time out')
                return render(request, 'main/message.html')

# BOOKING
class BookingList(APIView):
    # Api endpoint for view all Bookings.
    def get(self, request, format=None):
        booking = Booking.objects.all()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)

class BookingDetail(APIView):
    # Api endpoint for retrieve Booking instance.
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

class BookingCreate(APIView):
    def post(self, request, park_id, format=None):
        try:
            park = Park.objects.get(id=park_id)
        except:
            park = None
        if park == None: return Response({"message": "Please select a valid park to booking in!"})
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(park=park)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingUpdate(APIView):
    # Api endpoint for update Booking instance.
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDelete(APIView):
    # Api endpoint for delete Booking instance.
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        booking = self.get_object(pk)
        booking.delete()
        return Response({"message": "Booking info deleted!"}, status=status.HTTP_204_NO_CONTENT)

class ContactUsAPI(APIView):
    def post(self, request, format=None):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            email = data.get('email')
            name = data.get('name')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'Email from {name}', f"{email} \n\n {message}", email, [EMAIL_HOST_USER,], fail_silently=False)
            return Response({"message": "Contact message sent!"})
        return Response({"message": "Message not sent!"}, status=status.HTTP_400_BAD_REQUEST)

class SearchAutocomplete(APIView):
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

class Search(APIView):
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