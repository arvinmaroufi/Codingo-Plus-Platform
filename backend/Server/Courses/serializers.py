from rest_framework import serializers
from .models import (
    MainCategory, SubCategory, Tag, Course, CourseContent,
    CourseFaq, CourseChapter, CourseSession, Comment, CommentReply
)



class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        # All fields are writable except the auto-managed timestamps


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = (
            'created_at', 'updated_at', 'enrollment_count',
            'average_rating', 'review_count', 'views', 'published_date'
        )


class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFaq
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSession
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'likes', 'popular_comment')


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
