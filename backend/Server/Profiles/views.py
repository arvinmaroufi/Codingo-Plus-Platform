from django.shortcuts import get_object_or_404

from rest_framework.views import Response, APIView
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser


from .models import AdminProfile, StudentProfile, TeacherProfile, SupporterProfile
from .serializers import AdminProfileSerializer, StudentProfileSerializer, TeacherProfileSerializer, SupporterProfileSerializer
from .permissions import IsProfileOwnerOrAdmin




class AdminProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAdminUser]
    lookup_field = "username"

    def list(self, request):
        queryset = AdminProfile.objects.all()
        serializer = AdminProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, username):
        query = get_object_or_404(AdminProfile, user__username=username)
        serializer = AdminProfileSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, username):
        instance = get_object_or_404(AdminProfile, user__username=username)
        serializer = AdminProfileSerializer(instance, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class StudentProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsProfileOwnerOrAdmin]
    lookup_field = "username"

    def list(self, request):
        queryset = StudentProfile.objects.all()
        serializer = StudentProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, username):
        query = get_object_or_404(StudentProfile, user__username=username)
        serializer = StudentProfileSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, username):
        instance = get_object_or_404(StudentProfile, user__username=username)
        serializer = StudentProfileSerializer(instance, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class TeacherProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsProfileOwnerOrAdmin]
    lookup_field = "username"

    def list(self, request):
        queryset = TeacherProfile.objects.all()
        serializer = TeacherProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, username):
        query = get_object_or_404(TeacherProfile, user__username=username)
        serializer = TeacherProfileSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, username):
        instance = get_object_or_404(TeacherProfile, user__username=username)
        serializer = TeacherProfileSerializer(instance, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class SupporterProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsProfileOwnerOrAdmin]
    lookup_field = "username"

    def list(self, request):
        queryset = SupporterProfile.objects.all()
        serializer = SupporterProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, username):
        query = get_object_or_404(SupporterProfile, user__username=username)
        serializer = SupporterProfileSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, username):
        instance = get_object_or_404(SupporterProfile, user__username=username)
        serializer = SupporterProfileSerializer(instance, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
