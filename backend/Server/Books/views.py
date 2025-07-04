from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import MainCategory, SubCategory, Tag
from .serializers import MainCategorySerializer, SubCategorySerializer, TagSerializer
from .permissions import IsAdminOrReadOnly




class MainCategoryViewSet(ViewSet):

    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    
    def list(self):
        queryset = MainCategory.objects.all()
        serializer = MainCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = MainCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The MainCategory is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        serializer = MainCategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The MainCategory is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'The MainCategory is deleted.'}, status=status.HTTP_204_NO_CONTENT)



class SubCategoryViewSet(ViewSet):

    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    
    def list(self):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The SubCategory is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        serializer = SubCategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The SubCategory is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'The SubCategory is deleted.'}, status=status.HTTP_204_NO_CONTENT)



class TagViewSet(ViewSet):

    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    
    def list(self):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The Tag is added.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, slug):
        instance = get_object_or_404(Tag, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        serializer = TagSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'The Tag is updated.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, slug):
        instance = get_object_or_404(Tag, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'The Tag is deleted.'}, status=status.HTTP_204_NO_CONTENT)
