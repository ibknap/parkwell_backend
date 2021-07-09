from main.serializers import BookingSerializer
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import Http404
from rest_framework import status
from main.models import Booking
from park.models import Park

class Main(TemplateView):
    template_name = "main/main.html"

class Docs(TemplateView):
    template_name = "main/docs.html"
    
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