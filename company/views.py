# from rest_framework.permissions import IsAuthenticated
from account.models import CompanyAdminProfile
from rest_framework.response import Response
from .serializers import CompanySerializer
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import Company

# COMPANY
class CompanyList(APIView):
    # Api endpoint for view all Company.
    def get(self, request, format=None):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return Response(serializer.data)

class CompanyDetail(APIView):
    # Api endpoint for retrieve Company instance.
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

class CompanyCreate(APIView):
    # permission_classes = [IsAuthenticated,]
    
    def post(self, request, user_id, format=None):
        try:
            admin = CompanyAdminProfile.objects.get(admin=user_id)
        except:
            admin = None
        if admin == None: return Response({"message": "User is not a company admin!"})
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(admin=admin)
            except:
                return Response({"message": f"Company admin associated with a company!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyUpdate(APIView):
    # Api endpoint for update Company instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyDelete(APIView):
    # Api endpoint for delete Company instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        company = self.get_object(pk)
        company.delete()
        return Response({"message": "Company deleted!"}, status=status.HTTP_204_NO_CONTENT)