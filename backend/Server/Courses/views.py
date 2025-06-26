from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.views import APIView, Response

from .models import MainCategory, SubCategory, Tag, Course, CourseFaq
from .serializers import MainCategorySerializer, SubCategorySerializer, TagSerializer, CourseSerializer, CourseFaqSerializer
from .permissions import IsAdminOrReadOnly, CoursePermission, IsCourseTeacherOrAdmin





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



class CourseViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [CoursePermission]

    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, slug):
        instance = get_object_or_404(Course, slug=slug)
        serilizer = CourseSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The main category is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, slug):
        if request.user.is_authenticated:
            instance = get_object_or_404(Course, slug=slug)
            serializer = CourseSerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                self.check_object_permissions(request=request, obj=instance)
                serializer.save()
                return Response({'massage': 'The main category is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, slug):
        if request.user.is_authenticated:
            instance = get_object_or_404(Course, slug=slug)
            if request.user == instance.author or request.user.is_staff:
                self.check_object_permissions(request=request, obj=instance)
                instance.delete()
                return Response({'massage': 'The main category is deleted.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You dont have any fucking permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)    
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)
        


        
class CourseFaqViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [IsCourseTeacherOrAdmin]

    def list(self, request):
        queryset = CourseFaq.objects.all()
        serializer = CourseFaqSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, pk):
        instance = get_object_or_404(CourseFaq, id=pk)
        serilizer = CourseFaqSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseFaqSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The main category is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseFaq, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CourseFaqSerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The main category is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseFaq, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The main category is deleted.'}, status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def course_faqs(self, request, slug):
        instance = get_object_or_404(Course, slug)
        queryset = CourseFaq.obje.filter(course=instance)
        serializer = CourseFaqSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    