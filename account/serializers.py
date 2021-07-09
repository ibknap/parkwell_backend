from account.models import CompanyAdminProfile, ParkAdminProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
import re

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 2

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email =  serializers.EmailField(style={"input_type": "email"}, write_only=True)
    password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        extra_kwargs = {'password1': {'write_only': True}}
    
    # Validation
    def validate_password(self, password1):
        password_regex = re.search('[A-Z]', password1) is None or re.search('[0-9]', password1) is None
        error_message = 'Your password must contain at least 1 number, and 1 uppercase'
        if password_regex: raise serializers.ValidationError(error_message)

    # overriding save method
    def save(self):
        user = User(email=self.validated_data['email'], username=self.validated_data['username'])
        password1 = self.validated_data['password1']
        username_exist = User.objects.filter(username=self.validated_data['username']).exists()
        email_exist = User.objects.filter(email=self.validated_data['email']).exists()

        if username_exist: raise serializers.ValidationError({'username': 'Username already exist!!!'})
        if email_exist: raise serializers.ValidationError({'email': 'Email already exist!!!'})

        # setting password after validation and save user registeration data
        user.set_password(password1)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(style={"input_type": "text"}, write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
        
    # Validation
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        request = self.context.get("request")

        if username and password:
            user = authenticate(request=request, username=username, password=password)
            if not user:
                message = "Unable to login with provided credentials!"
                raise serializers.ValidationError(message, code="authorization")
        else:
            message = "Must include your username and password!"
            raise serializers.ValidationError(message, code="authorization")

        data["user"] = user
        return data


class CompanyAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAdminProfile
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        return CompanyAdminProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company_admin_photo = validated_data.get('company_admin_photo', instance.company_admin_photo)
        instance.company_admin_number = validated_data.get('company_admin_number', instance.company_admin_number)
        instance.save()
        return instance

class ParkAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkAdminProfile
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        return ParkAdminProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.park_admin_photo = validated_data.get('park_admin_photo', instance.park_admin_photo)
        instance.park_admin_number = validated_data.get('park_admin_number', instance.park_admin_number)
        instance.save()
        return instance