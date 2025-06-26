from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Department, Ticket, TicketMessage, TicketAttachment, CourseDepartment, CourseTicket
from .serializers import DepartmentSerializer, TicketSerializer, TicketMessageSerializer, TicketAttachmentSerializer, CourseDepartmentSerializer, CourseTicketSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrUser


    
    
class DepartmentViewSet(ViewSet):

    permission_classes = [IsAdminOrReadOnly]
    
    def list(self):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The Department is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, slug):
        instance = get_object_or_404(Department, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        serializer = DepartmentSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The Department is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, slug):
        instance = get_object_or_404(Department, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'The Department is deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
    
class TicketViewSet(ViewSet):
    
    permission_classes = [IsAdminOrUser]
    lookup_field = 'pk'

    def list(self, request):
        queryset = Ticket.objects.all()
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = TicketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Ticket created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        self.check_object_permissions(request, ticket)
        ticket.delete()
        return Response({'message': 'Ticket deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class TicketMessageViewSet(ViewSet):
    permission_classes = [IsAdminOrUser]
    lookup_field = 'pk'

    def list(self, request):
        queryset = TicketMessage.objects.all()
        serializer = TicketMessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        message = get_object_or_404(TicketMessage, pk=pk)
        serializer = TicketMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = TicketMessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'TicketMessage created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        message = get_object_or_404(TicketMessage, pk=pk)
        self.check_object_permissions(request, message)
        message.delete()
        return Response({'message': 'TicketMessage deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

class TicketAttachmentViewSet(ViewSet):
    permission_classes = [IsAdminOrUser]
    lookup_field = 'pk'

    def list(self, request):
        queryset = TicketAttachment.objects.all()
        serializer = TicketAttachmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        attachment = get_object_or_404(TicketAttachment, pk=pk)
        serializer = TicketAttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = TicketAttachmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'TicketAttachment created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        attachment = get_object_or_404(TicketAttachment, pk=pk)
        self.check_object_permissions(request, attachment)
        attachment.delete()
        return Response({'message': 'TicketAttachment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    
class CourseDepartmentViewSet(ViewSet):

    permission_classes = [IsAdminOrReadOnly]
    
    def list(self):
        queryset = CourseDepartment.objects.all()
        serializer = CourseDepartmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = CourseDepartmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The CourseDepartment is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, slug):
        instance = get_object_or_404(CourseDepartment, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        serializer = CourseDepartmentSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The CourseDepartment is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, slug):
        instance = get_object_or_404(CourseDepartment, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'The CourseDepartment is deleted.'}, status=status.HTTP_204_NO_CONTENT)
    

class CourseTicketViewSet(ViewSet):
    permission_classes = [IsAdminOrUser]
    lookup_field = 'pk'

    def list(self, request):
        queryset = CourseTicket.objects.all()
        serializer = CourseTicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        ticket = get_object_or_404(CourseTicket, pk=pk)
        serializer = CourseTicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CourseTicketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'CourseTicket created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        ticket = get_object_or_404(CourseTicket, pk=pk)
        self.check_object_permissions(request, ticket)
        serializer = CourseTicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'CourseTicket updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        ticket = get_object_or_404(CourseTicket, pk=pk)
        self.check_object_permissions(request, ticket)
        ticket.delete()
        return Response({'message': 'CourseTicket deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
