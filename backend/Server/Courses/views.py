from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.views import APIView, Response

from .permissions import IsAdminOrReadOnly, CoursePermission, IsCourseTeacherOrAdmin, CourseSessionsPermission, CommentsPermission
from .serializers import *
from .filters import CourseFilter



class MainCategoryViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = MainCategory.objects.all()
        serializer = MainCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        serilizer = MainCategorySerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MainCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'دسته بندی ایجاد شد.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        serializer = MainCategorySerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.check_object_permissions(request=request, obj=instance)
            serializer.save()
            return Response({'message': 'دسته بندی آپدیت شد.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        instance = get_object_or_404(MainCategory, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'دسته بندی اصلی  حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
        

class SubCategoryViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        serilizer = SubCategorySerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = SubCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'دسته بندی زیر مجموعه ایجاد شد.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        serializer = SubCategorySerializer(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.check_object_permissions(request=request, obj=instance)
            serializer.save()
            return Response({'message': 'دسته بندی زیر مجموعه آپدیت شد.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        instance = get_object_or_404(SubCategory, slug=slug)
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()
        return Response({'message': 'دسته بندی زیر مجموعه حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
    


class TagViewSet(viewsets.ViewSet):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug):
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
        # 1. Base queryset
        qs = Course.objects.all()

        # 2. Apply django-filter filters
        filtered = CourseFilter(request.GET, queryset=qs)
        qs = filtered.qs

        # 3. Handle ordering (defaulting to -published_date)
        order_by = request.query_params.get('order_by', '-published_date')
        # optional: validate order_by against an allowed list
        allowed = {'price','-price','published_date','-published_date','views','-views'}
        if order_by in allowed:
            qs = qs.order_by(order_by)

        # 4. Serialize and return
        serializer = CourseSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, slug):
        instance = get_object_or_404(Course, slug=slug)
        serilizer = CourseSerializer(instance, context={'request': request})
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'detail': 'دوره ایجاد شد.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'errors:': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': "شما برای انجام این عملیات باید اول احراز حویت کنید."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, slug):
        if request.user.is_authenticated:
            instance = get_object_or_404(Course, slug=slug)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CourseSerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'detail': 'دوره آپدیت شد.'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors:': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': "شما برای انجام این عملیات باید اول احراز حویت کنید."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, slug):
        if request.user.is_authenticated:
            instance = get_object_or_404(Course, slug=slug)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'detail': 'دوره حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': "شما برای انجام این عملیات باید اول احراز حویت کنید."}, status=status.HTTP_401_UNAUTHORIZED)
        

        

        

        
class CourseContentViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [IsCourseTeacherOrAdmin]

    def list(self, request):
        queryset = CourseContent.objects.all()
        serializer = CourseContentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
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
    
    def retrieve(self, request, pk):
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
    
    def retrieve(self, request, pk):
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
        serializer = CourseSessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(CourseSession, id=pk)
        serilizer = CourseSessionSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CourseSessionSerializer(data=request.data, context={'request': request})
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
            serializer = CourseSessionSerializer(instance, data=request.data, context={'request': request}, partial=True)
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
        serializer = CourseSessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def course_sessions(self, request, pk):
        instance = get_object_or_404(Course, id=pk)
        queryset = CourseSession.objects.filter(chapter__course=instance)
        serializer = CourseSessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CommentViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [CommentsPermission]

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(Comment, id=pk)
        serilizer = CommentSerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The comment is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(Comment, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CommentSerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The comment is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(Comment, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The comment is deleted.'}, status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def course_comments(self, request, slug):
        instance = get_object_or_404(Course, slug=slug)
        queryset = Comment.objects.filter(course=instance)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CommentReplayViewSet(viewsets.ViewSet):

    lookup_field = 'pk'
    permission_classes = [CommentsPermission]

    def list(self, request):
        queryset = CommentReply.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(CommentReply, id=pk)
        serilizer = CommentReplySerializer(instance)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = CommentReplySerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The replay is created.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CommentReply, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            serializer = CommentReplySerializer(instance, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'massage': 'The replay is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(CommentReply, id=pk)
            self.check_object_permissions(request=request, obj=instance)
            instance.delete()
            return Response({'massage': 'The replay is deleted.'}, status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({'massage': "You need to autherize for performing this action."}, status=status.HTTP_401_UNAUTHORIZED)

    def comment_replays(self, request, pk):
        instance = get_object_or_404(Comment, id=pk)
        queryset = CommentReply.objects.filter(comment=instance)
        serializer = CommentReplySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)