from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer
from .permissions import IsAdminOrReadOnly


    
    
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