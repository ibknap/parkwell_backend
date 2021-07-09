from .serializers import ParkOtherServiceSerializer, ParkSerializer, ParkImageSerializer
# from rest_framework.permissions import IsAuthenticated
from .models import Park, ParkImage, ParkOtherService
from account.models import CompanyAdminProfile, ParkAdminProfile
from rest_framework.response import Response
from rest_framework.views import APIView
from company.models import Company
from rest_framework import status
from django.http import Http404

# PARK
class ParkList(APIView):
    # Api endpoint for view all Parks.
    def get(self, request, format=None):
        park = Park.objects.all()
        serializer = ParkSerializer(park, many=True)
        return Response(serializer.data)

class ParkDetail(APIView):
    # Api endpoint for retrieve Park instance.
    def get_object(self, pk):
        try:
            return Park.objects.get(pk=pk)
        except Park.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        park = self.get_object(pk)
        serializer = ParkSerializer(park)
        return Response(serializer.data)

class ParkCreate(APIView):
    # permission_classes = [IsAuthenticated,]

    def post(self, request, user_id, format=None):
        try:
            park_admin = ParkAdminProfile.objects.get(admin=user_id)
        except:
            park_admin = None
        if park_admin == None: return Response({"message": "User is not a park admin!"})

        try:
            company = Company.objects.get(admin=park_admin.company_admin)
        except:
            company = None
        if company == None: return Response({"message": "Company admin not associated with a company!"})
        
        serializer = ParkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(company=company, admin=park_admin)
            except:
                return Response({"message": f"Park admin associated with a park!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkUpdate(APIView):
    # Api endpoint for update Park instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return Park.objects.get(pk=pk)
        except Park.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        park = self.get_object(pk)
        serializer = ParkSerializer(park, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkDelete(APIView):
    # Api endpoint for delete Park instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return Park.objects.get(pk=pk)
        except Park.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        park = self.get_object(pk)
        park.delete()
        return Response({"message": "Park deleted!"}, status=status.HTTP_204_NO_CONTENT)

# PARK IMAGES
class ParkImageList(APIView):
    # Api endpoint for view all ParkImages.
    def get(self, request, format=None):
        park_image = ParkImage.objects.all()
        serializer = ParkImageSerializer(park_image, many=True)
        return Response(serializer.data)

class ParkImageDetail(APIView):
    # Api endpoint for retrieve ParkImage instance.
    def get_object(self, pk):
        try:
            return ParkImage.objects.get(pk=pk)
        except ParkImage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        park_image = self.get_object(pk)
        serializer = ParkImageSerializer(park_image)
        return Response(serializer.data)

class ParkImageCreate(APIView):
    # permission_classes = [IsAuthenticated,]

    def post(self, request, park_id, format=None):
        park = Park.objects.get(id=park_id)
        serializer = ParkImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(park=park)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkImageUpdate(APIView):
    # Api endpoint for update ParkImage instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return ParkImage.objects.get(pk=pk)
        except ParkImage.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        park_image = self.get_object(pk)
        serializer = ParkImageSerializer(park_image, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkImageDelete(APIView):
    # Api endpoint for delete ParkImage instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return ParkImage.objects.get(pk=pk)
        except ParkImage.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        park_image = self.get_object(pk)
        park_image.delete()
        return Response({"message": "Park image deleted!"}, status=status.HTTP_204_NO_CONTENT)

# PARK OTHER SERVICES
class ParkOtherServiceList(APIView):
    # Api endpoint for view all ParkOtherServices.
    def get(self, request, format=None):
        park_service = ParkOtherService.objects.all()
        serializer = ParkOtherServiceSerializer(park_service, many=True)
        return Response(serializer.data)

class ParkOtherServiceDetail(APIView):
    # Api endpoint for retrieve ParkOtherService instance.
    def get_object(self, pk):
        try:
            return ParkOtherService.objects.get(pk=pk)
        except ParkOtherService.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        park_service = self.get_object(pk)
        serializer = ParkOtherServiceSerializer(park_service)
        return Response(serializer.data)

class ParkOtherServiceCreate(APIView):
    # permission_classes = [IsAuthenticated,]

    def post(self, request, park_id, format=None):
        park = Park.objects.get(id=park_id)
        
        serializer = ParkOtherServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(park=park)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkOtherServiceUpdate(APIView):
    # Api endpoint for update ParkOtherService instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return ParkOtherService.objects.get(pk=pk)
        except ParkOtherService.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        park_service = self.get_object(pk)
        serializer = ParkOtherServiceSerializer(park_service, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParkOtherServiceDelete(APIView):
    # Api endpoint for delete ParkOtherService instance.
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self, pk):
        try:
            return ParkOtherService.objects.get(pk=pk)
        except ParkOtherService.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        park_service = self.get_object(pk)
        park_service.delete()
        return Response({"message": "Park other service deleted!"}, status=status.HTTP_204_NO_CONTENT)
