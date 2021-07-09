from .models import Park, ParkImage, ParkOtherService
from rest_framework import serializers

class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Park
        fields = '__all__'
        depth = 3
    
    def create(self, validated_data):
        return Park.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.park_name = validated_data.get('park_name', instance.park_name)
        instance.park_email = validated_data.get('park_email', instance.park_email)
        instance.free_space = validated_data.get('free_space', instance.free_space)
        instance.park_number = validated_data.get('park_number', instance.park_number)
        instance.park_address = validated_data.get('park_address', instance.park_address)
        instance.park_coordinates = validated_data.get('park_coordinates', instance.park_coordinates)
        instance.park_about = validated_data.get('park_about', instance.park_about)
        instance.save()
        return instance

class ParkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkImage
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        return ParkImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.park_images = validated_data.get('park_images', instance.park_images)
        instance.save()
        return instance

class ParkOtherServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkOtherService
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        return ParkOtherService.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.park_service = validated_data.get('park_service', instance.park_service)
        instance.save()
        return instance