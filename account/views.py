from .serializers import AdminLoginSerializer, CompanyAdminProfileSerializer, LoginSerializer, ParkAdminProfileSerializer, RegisterSerializer, UserSerializer
from account.models import CompanyAdminProfile, ParkAdminProfile
# from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

# USER
class UserList(APIView):
    # Api endpoint for view all User.
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    # Api endpoint for retrieve User instance.
    def get_object(self, token):
        try:
            return Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise Http404

    def get(self, request, token, format=None):
        user = self.get_object(token)
        serializer = UserSerializer(user.user)
        return Response(serializer.data)

class UserUpdate(APIView):
    # Api endpoint for update User instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDelete(APIView):
    # Api endpoint for delete User instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response({"message": "User deleted!"}, status=status.HTTP_204_NO_CONTENT)

# REGISTER
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    data = {}

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = Token.objects.get(user=user).key
            self.data['message'] = "Successfully registered new user!"
            self.data['username'] = user.username
            self.data['email'] = user.email
            self.data['user_id'] = user.id
            self.data['token'] = token
        else:
            self.data = serializer.errors
        return Response(self.data)

class RegisterAsCompanyAdminAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    data = {}

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = Token.objects.get(user=user).key
            self.data['message'] = "Successfully registered as company admin!"
            self.data['username'] = user.username
            self.data['email'] = user.email
            self.data['user_id'] = user.id
            self.data['token'] = token

            serializer = CompanyAdminProfileSerializer(data=request.data)
            if CompanyAdminProfile.objects.filter(admin=user).exists():
                message = {"message": "User already has a company admin profile"}
                return Response(message)

            if serializer.is_valid(raise_exception=True):
                serializer.save(admin=user)
                return Response(self.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.data = serializer.errors
        return Response(self.data)

# LOGIN
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    data = {}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            token = Token.objects.get(user=user)
            self.data['message'] = "Login successful!"
            self.data['user_id'] = user.id
            self.data['email'] = user.email
            self.data['token'] = token.key
            return Response(self.data, status=status.HTTP_200_OK)

# ADMIN LOGIN
class AdminLoginAPI(GenericAPIView):
    serializer_class = AdminLoginSerializer
    data = {}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            token = Token.objects.get(user=user)
            self.data['message'] = "Login as admin successful!"
            self.data['user_id'] = user.id
            self.data['email'] = user.email
            self.data['token'] = token.key
            return Response(self.data, status=status.HTTP_200_OK)

# LOGOUT
class LogoutAPI(APIView):
    # permission_classes = [IsAuthenticated,]
    data = {}

    def post(self, request):
        logout(request)
        self.data["message"] = "Logout successful!"
        return Response(self.data, status=status.HTTP_200_OK)

# COMPANY ADMIN PROFILE
class CompanyAdminProfileList(APIView):
    # Api endpoint for view all CompanyAdminProfile.
    def get(self, request, format=None):
        company_admin_profile = CompanyAdminProfile.objects.all()
        serializer = CompanyAdminProfileSerializer(company_admin_profile, many=True)
        return Response(serializer.data)

class CompanyAdminProfileDetail(APIView):
    # Api endpoint for retrieve CompanyAdminProfile instance.
    def get_object(self, user_id):
        try:
            return CompanyAdminProfile.objects.get(admin=user_id)
        except CompanyAdminProfile.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        company_admin_profile = self.get_object(user_id)
        serializer = CompanyAdminProfileSerializer(company_admin_profile)
        return Response(serializer.data)

class CompanyAdminProfileCreate(APIView):
    def post(self, request, user_id, format=None):
        serializer = CompanyAdminProfileSerializer(data=request.data)
        user = User.objects.get(id=user_id)
        if CompanyAdminProfile.objects.filter(admin=user).exists():
            message = {"message": "User already has a company admin profile"}
            return Response(message)

        if serializer.is_valid(raise_exception=True):
            serializer.save(admin=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyAdminProfileUpdate(APIView):
    # Api endpoint for update CompanyAdminProfile instance.
    def get_object(self, pk):
        try:
            return CompanyAdminProfile.objects.get(pk=pk)
        except CompanyAdminProfile.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        company_admin_profile = self.get_object(pk)
        serializer = CompanyAdminProfileSerializer(company_admin_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyAdminProfileDelete(APIView):
    # Api endpoint for delete CompanyAdminProfile instance.
    def get_object(self, pk):
        try:
            return CompanyAdminProfile.objects.get(pk=pk)
        except CompanyAdminProfile.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        company_admin_profile = self.get_object(pk)
        company_admin_profile.delete()
        return Response({"message": "Company admin deleted!"}, status=status.HTTP_204_NO_CONTENT)

# PARK ADMIN PROFILE
class ParkAdminProfileList(APIView):
    # Api endpoint for view all ParkAdminProfile.
    def get(self, request, format=None):
        park_admin_profile = ParkAdminProfile.objects.all()
        serializer = ParkAdminProfileSerializer(park_admin_profile, many=True)
        return Response(serializer.data)

class ParkAdminProfileDetail(APIView):
    # Api endpoint for retrieve ParkAdminProfile instance.
    def get_object(self, user_id):
        try:
            return ParkAdminProfile.objects.get(admin=user_id)
        except ParkAdminProfile.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        park_admin_profile = self.get_object(user_id)
        serializer = ParkAdminProfileSerializer(park_admin_profile)
        return Response(serializer.data)

class ParkAdminProfileCreate(APIView):
    def post(self, request, user_id, company_admin, format=None):
        serializer = ParkAdminProfileSerializer(data=request.data)
        user = User.objects.get(id=user_id)
        company_admin_inst = CompanyAdminProfile.objects.get(id=company_admin)
        if ParkAdminProfile.objects.filter(admin=user).exists():
            message = {"message": "User already has a park admin profile"}
            return Response(message)

        if serializer.is_valid(raise_exception=True):
            serializer.save(admin=user, company_admin=company_admin_inst)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkAdminProfileUpdate(APIView):
    # Api endpoint for update ParkAdminProfile instance.
    def get_object(self, pk):
        try:
            return ParkAdminProfile.objects.get(pk=pk)
        except ParkAdminProfile.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        park_admin_profile = self.get_object(pk)
        serializer = ParkAdminProfileSerializer(park_admin_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkAdminProfileDelete(APIView):
    # Api endpoint for delete ParkAdminProfile instance.
    def get_object(self, pk):
        try:
            return ParkAdminProfile.objects.get(pk=pk)
        except ParkAdminProfile.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        park_admin_profile = self.get_object(pk)
        park_admin_profile.delete()
        return Response({"message": "Park admin deleted!"}, status=status.HTTP_204_NO_CONTENT)