from django.db.models.fields import DateTimeField
from park.serializers import ParkSerializer
from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        depth = 3
    
    def create(self, validated_data):
        return Booking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.park = validated_data.get('park', instance.park)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.arrival_time = validated_data.get('arrival_time', instance.arrival_time)
        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.save()
        return instance

class ContactUsSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()