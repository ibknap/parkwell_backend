from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company_logo = validated_data.get('company_logo', instance.company_logo)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.company_email = validated_data.get('company_email', instance.company_email)
        instance.company_number = validated_data.get('company_number', instance.company_number)
        instance.company_about = validated_data.get('company_about', instance.company_about)
        instance.save()
        return instance