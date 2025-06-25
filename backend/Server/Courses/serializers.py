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

    def create(self, validated_data):
        return MainCategory.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.description = validated_data.get('description', instance.description)
        instance.color_code = validated_data.get('color_code', instance.color_code)
        instance.save()
        
        return instance


class SubCategorySerializer(serializers.ModelSerializer):

    main_category_slug = serializers.CharField(write_only=True, required=False)

    parent = MainCategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'parent')


    def create(self, validated_data):
        

        slug = validated_data.pop('slug', None)
        if slug is None:
            raise serializers.ValidationError({'slug': 'slug is needed.'})
        
        title = validated_data.pop('title', None)
        if title is None:
            raise serializers.ValidationError({'title': 'title is needed.'})

        main_category_slug = validated_data.pop('main_category_slug', None)
        if main_category_slug is None:
            raise serializers.ValidationError({'main_category_slug': 'The main_category_slug is needed.'})
        
        try:
            main_category = MainCategory.objects.get(slug=main_category_slug)
        except MainCategory.DoesNotExist:
            raise serializers.ValidationError({'main_category_slug': 'The main category slug is not exists.'})

        query = SubCategory.objects.create(
            parent=main_category,
            title=title,
            slug=slug
            **validated_data
        )

        query.save()

        return query


    def update(self, instance, validated_data):
        main_category_slug = validated_data.pop('main_category_slug', None)

        if main_category_slug:
            try:
                main_category = MainCategory.objects.get(slug=main_category_slug)
                instance.parent = main_category
            except MainCategory.DoesNotExist:
                raise serializers.ValidationError({'main_category_slug': 'The main category slug is not exists.'})

        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.banner = validated_data.get('banner', instance.banner)
        instance.description = validated_data.get('description', instance.description)

        instance.save()

        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        query = Tag.objects.create(**validated_data)
        query.save()
        return query
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)

        instance.save()
        return instance


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
