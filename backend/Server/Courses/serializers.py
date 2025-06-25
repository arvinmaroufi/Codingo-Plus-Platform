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

    tags = TagSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'enrollment_count', 'average_rating', 'review_count', 'views', 'teacher')


    def create(self, validated_data):

        request = self.context.get('request')
        teacher = request.user

        category_slug = validated_data.pop('category_slug', None)
        if category_slug is not None:
            try:
                category = SubCategory.objects.get(slug=category_slug)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({'category_slug': 'The category_slug is not founded.'})
        else:
            raise serializers.ValidationError({'category_slug': 'The category is needed.'})
        
        slug = validated_data.pop('slug', None)
        if slug is None:
            raise serializers.ValidationError({'slug': 'slug is needed.'})
        
        title = validated_data.pop('title', None)
        if title is None:
            raise serializers.ValidationError({'title': 'title is needed.'})
        
        level_status = validated_data.pop('level_status', None)
        if level_status is None:
            raise serializers.ValidationError({'level_status': 'level_status is needed.'})
        
        payment_status = validated_data.pop('payment_status', None)
        if payment_status is None:
            raise serializers.ValidationError({'payment_status': 'payment_status is needed.'})
        
        status = validated_data.pop('status', None)
        if status is None:
            raise serializers.ValidationError({'status': 'status is needed.'})
        
        language = validated_data.pop('language', None)
        if language is None:
            raise serializers.ValidationError({'language': 'language is needed.'})
        

        price = validated_data.pop('price', None)
        
        if payment_status == "P" and price is None:
            raise serializers.ValidationError({'price': 'The price is required when you want to make the course premuim'})
            
        validated_data['is_recommended'] = False

        query = Course.objects.create(
            teacher=teacher,
            category=category,
            **validated_data
        )
        
        query.save()
        
        return query


    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request.user.is_staff:
            instance.is_recommended = validated_data.get('is_recommended', instance.is_recommended)
        
        # Core fields
        instance.slug = validated_data.get('slug', instance.slug)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.short_description = validated_data.get('short_description', instance.short_description)

        # Contant details
        instance.prerequisites = validated_data.get('prerequisites', instance.prerequisites)
        instance.learning_outcomes = validated_data.get('learning_outcomes', instance.learning_outcomes)
        instance.duration = validated_data.get('duration', instance.duration)

        # Pricing
        instance.price = validated_data.get('price', instance.price)
        instance.payment_ststus = validated_data.get('payment_ststus', instance.payment_ststus)

        # Media
        instance.poster = validated_data.get('poster', instance.poster)
        instance.banner = validated_data.get('banner', instance.banner)
        instance.trailer = validated_data.get('trailer', instance.trailer)

        # Metadata 
        instance.status = validated_data.get('status', instance.status)
        instance.level_status = validated_data.get('level_status', instance.level_status)
        instance.course_status = validated_data.get('course_status', instance.course_status)
        instance.has_certificate = validated_data.get('has_certificate', instance.has_certificate)

        # Timestamps
        instance.published_date = validated_data.get('published_date', instance.published_date)

        category_slug = validated_data.pop('category_slug', None)
        if category_slug is not None:
            try:
                category = SubCategory.objects.get(slug=category_slug)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({'category_slug': 'The category_slug is not founded.'})

        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        instance.save()
        return instance
    


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
