from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Blog, MainCategory
from .serializers import BlogSerializer, MainCategorySerializer
from .permissions import IsAdminOrAuthor, IsAdminOrReadOnly




class BlogViewSet(ViewSet):

    permission_classes =[IsAdminOrAuthor]
    lookup_field = 'slug'

    def list(self, request):
        if request.user.is_staff:
            queryset = Blog.objects.all()
        else:
            queryset = Blog.objects.filter(status="PD")
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, slug):
        if request.user.is_staff:
            query = get_object_or_404(Blog, slug=slug)
        else:
            query = get_object_or_404(Blog, slug=slug, status="PD")
        serializer = BlogSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        serializer = BlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'massage': 'The blog is created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'massage': 'The blog is updated.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        query = get_object_or_404(Blog, slug=slug)
        if request.user == query.author or request.user.is_staff:
            query.delete()
            return Response({'massage': 'The blog is deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You dont have any fucking permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        

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
