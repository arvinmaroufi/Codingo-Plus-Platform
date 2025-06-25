from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.views import APIView, Response

from .models import MainCategory, SubCategory, Tag
from .serializers import MainCategorySerializer, SubCategorySerializer, TagSerializer
from .permissions import IsAdminOrReadOnly





class MainCategoryViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = MainCategory.objects.all()
        serializer = MainCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        serilizer = MainCategorySerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MainCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'massage': 'The main category is created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        serializer = MainCategorySerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.check_object_permissions(request=request, obj=instance)
            serializer.save()
            return Response({'massage': 'The main category is updated.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        if request.user == instance.author or request.user.is_staff:
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The main category is deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You dont have any fucking permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        

class SubCategoryViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        serilizer = SubCategorySerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = SubCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'massage': 'The main category is created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        serializer = SubCategorySerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.check_object_permissions(request=request, obj=instance)
            serializer.save()
            return Response({'massage': 'The main category is updated.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        if request.user == instance.author or request.user.is_staff:
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The main category is deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You dont have any fucking permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        


class TagViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, slug):
        instance = get_object_or_404(Tag, slug=slug)
        serilizer = TagSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = TagSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'massage': 'The main category is created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(Tag, slug=slug)
        serializer = TagSerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.check_object_permissions(request=request, obj=instance)
            serializer.save()
            return Response({'massage': 'The main category is updated.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        instance = get_object_or_404(Tag, slug=slug)
        if request.user == instance.author or request.user.is_staff:
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The main category is deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You dont have any fucking permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)