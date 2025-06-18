from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import Blog, MainCategory, SubCategory, Tag, CommentReply, Comment
from .serializers import BlogSerializer, MainCategorySerializer, SubCategorySerializer, TagSerializer, CommentReplySerializer, CommentSerializer
from .permissions import IsAdminOrAuthor, IsAdminOrReadOnly, IsAdminOrCommentAuthor




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
    
    
    
class CommentReplyViewSet(ViewSet):
    
    permission_classes = [IsAdminOrCommentAuthor]
    lookup_field = 'pk'

    def list(self, request, comment_pk=None):
        if comment_pk:
            queryset = CommentReply.objects.filter(comment__pk=comment_pk)
        else:
            queryset = CommentReply.objects.all()
        serializer = CommentReplySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        reply = get_object_or_404(CommentReply, pk=pk)
        serializer = CommentReplySerializer(reply)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, comment_pk=None):
        if comment_pk:
            request.data['comment'] = comment_pk
        serializer = CommentReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Reply created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        reply = get_object_or_404(CommentReply, pk=pk)
        self.check_object_permissions(request, reply)
        serializer = CommentReplySerializer(reply, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Reply updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        reply = get_object_or_404(CommentReply, pk=pk)
        self.check_object_permissions(request, reply)
        reply.delete()
        return Response({'message': 'Reply deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

class CommentViewSet(ViewSet):
    
    permission_classes = [IsAdminOrCommentAuthor]
    lookup_field = 'pk'

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Comment created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Comment updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)