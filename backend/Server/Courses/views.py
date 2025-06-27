from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.views import APIView, Response

from .models import MainCategory, SubCategory, Tag, Course, CourseFaq, CourseContent, CourseChapter, CourseSession
from .serializers import MainCategorySerializer, SubCategorySerializer, TagSerializer, CourseSerializer, CourseFaqSerializer, CourseContentSerializer, CourseChapterSerializer, CourseSessionSerializer
from .permissions import IsAdminOrReadOnly, CoursePermission, IsCourseTeacherOrAdmin, CourseSessionsPermission




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
        

        
class CourseContentViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [IsCourseTeacherOrAdmin]

    def list(self, request):
        queryset = CourseContent.objects.all()
        serializer = CourseContentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, pk):
        instance = get_object_or_404(CourseContent, id=pk)
        serilizer = CourseContentSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseContentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The main category is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseContent, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CourseContentSerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The main category is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseContent, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The main category is deleted.'}, status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def course_contents(self, request, slug):
        instance = get_object_or_404(Course, slug)
        queryset = CourseContent.obje.filter(course=instance)
        serializer = CourseContentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


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
        queryset = CourseFaq.objects.filter(course=instance)
        serializer = CourseFaqSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CourseChapterViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [IsCourseTeacherOrAdmin]

    def list(self, request):
        queryset = CourseChapter.objects.all()
        serializer = CourseChapterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, pk):
        instance = get_object_or_404(CourseChapter, id=pk)
        serilizer = CourseChapterSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseChapterSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The chapter is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseChapter, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CourseChapterSerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The chapter is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseChapter, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The chapter is deleted.'}, status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def course_chapters(self, request, slug):
        instance = get_object_or_404(Course, slug)
        queryset = CourseChapter.objects.filter(course=instance)
        serializer = CourseChapterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseSessionViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [CourseSessionsPermission]

    def list(self, request):
        queryset = CourseSession.objects.all()
        serializer = CourseSession(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retreive(self, request, pk):
        instance = get_object_or_404(CourseSession, id=pk)
        serilizer = CourseSession(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseSession(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The session is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseSession, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CourseSession(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The session is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CourseSession, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The session is deleted.'}, status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def course_chapter_sessions(self, request, pk):
        instance = get_object_or_404(CourseChapter, id=pk)
        queryset = CourseSession.objects.filter(chapter=instance)
        serializer = CourseSession(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def course_sessions(self, request, pk):
        instance = get_object_or_404(Course, id=pk)
        queryset = CourseSession.objects.filter(chapter__course=instance)
        serializer = CourseSession(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)