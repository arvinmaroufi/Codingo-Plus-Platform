from rest_framework import serializers
from .models import (
    MainCategory, SubCategory, Tag, Course, CourseContent,
    CourseFaq, CourseChapter, CourseSession, Comment, CommentReply
)

from Accounts.models import UserCourseEnrollment
from Users.serializers import UserSerializer


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
        instance.save()
        
        return instance

class SubCategorySerializer(serializers.ModelSerializer):

    main_category = serializers.SlugRelatedField(slug_field="title", read_only=True)
    main_category_slug = serializers.CharField(write_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


    def create(self, validated_data):
        slug = validated_data.pop('slug', None)
        if slug is None:
            raise serializers.ValidationError({'error': 'نامک را وارد کنید.'})

        title = validated_data.pop('title', None)
        if title is None:
            raise serializers.ValidationError({'error': 'عنوان را وارد کنید.'})

        main_category_slug = validated_data.pop('main_category_slug', None)
        if main_category_slug is not None:
            try:
                main_category = MainCategory.objects.get(slug=main_category_slug)
            except MainCategory.DoesNotExist:
                raise serializers.ValidationError({'error': 'دسته بندی یافت نشد'})
        else:
            raise serializers.ValidationError({'error': 'دسته بندی اصلی را وارد کنید.'})

        instance = SubCategory.objects.create(
            main_category=main_category,
            title=title,
            slug=slug,
            **validated_data
        )

        instance.save()

        return instance



    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.icon = validated_data.get('icon', instance.icon)

        main_category_slug = validated_data.pop('main_category_slug', None)
        if main_category_slug is not None:
            try:
                main_category = MainCategory.objects.get(slug=main_category_slug)
                instance.main_category = main_category
            except MainCategory.DoesNotExist:
                raise serializers.ValidationError({'error': 'دسته بندی یافت نشد'})
        

        instance.save()

        return instance


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = MainCategory
        fields = "__all__"

    def get_sub_categories(self, obj):
        queryset = SubCategory.objects.filter(main_category=obj)
        serializer = SubCategorySerializer(queryset, many=True)
        return serializer.data
    


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

    category = SubCategorySerializer(read_only=True)
    teacher = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    is_enrolled = serializers.SerializerMethodField()

    category_slug = serializers.CharField(required=False, write_only=True)

    enrollment_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

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
                raise serializers.ValidationError({'category_slug': 'دسته بندی یافت نشد.'})
        else:
            raise serializers.ValidationError({'category_slug': 'دسته بندی را وارد کنید.'})
            
        
        slug = validated_data.pop('slug', None)
        if slug is None:
            raise serializers.ValidationError({'slug': 'اسلاگ را وارد کنید.'})
        
        title = validated_data.pop('title', None)
        if title is None:
            raise serializers.ValidationError({'title': 'عنموان اجباری است.'})
        
        level_status = validated_data.pop('level_status', None)
        if level_status is None:
            raise serializers.ValidationError({'level_status': 'سطح دوره را وارد کنید.'})
        
        payment_status = validated_data.pop('payment_status', None)
        if payment_status is None:
            raise serializers.ValidationError({'payment_status': 'نوع پرداخت را وارد کنید.'})
        
        status = validated_data.pop('status', None)
        if status is None:
            raise serializers.ValidationError({'status': 'وضعیت را وارد کنید.'})
        
        language = validated_data.pop('language', None)
        if language is None:
            raise serializers.ValidationError({'language': 'زبان را وارد کنید.'})
        

        price = validated_data.pop('price', None)
        
        if payment_status == "P" and price is None:
            raise serializers.ValidationError({'price': 'اگر نوع پرداخت رایگان نباشد باید قیمت آن را وارد کنید.'})

        query = Course.objects.create(
            slug=slug,
            title=title,
            price=price,
            teacher=teacher,
            category=category,
            language=language,
            level_status=level_status,
            payment_status=payment_status,
        )
        
        query.save()
        
        return query


    def update(self, instance, validated_data):
        # Core fields
        instance.slug = validated_data.get('slug', instance.slug)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.language = validated_data.get('language', instance.language)

        # Pricing
        instance.price = validated_data.get('price', instance.price)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)

        # Media
        instance.poster = validated_data.get('poster', instance.poster)
        instance.banner = validated_data.get('banner', instance.banner)
        instance.trailer = validated_data.get('trailer', instance.trailer)

        # Metadata 
        instance.status = validated_data.get('status', instance.status)
        instance.level_status = validated_data.get('level_status', instance.level_status)
        instance.publish_status = validated_data.get('publish_status', instance.publish_status)

        # Timestamps
        instance.published_date = validated_data.get('published_date', instance.published_date)

        category_slug = validated_data.pop('category_slug', None)
        if category_slug is not None:
            try:
                category = SubCategory.objects.get(slug=category_slug)
                instance.category = category
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({'category_slug': 'دسته بندی یافت نشد.'})


        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        instance.save()
        return instance
    

    def get_is_enrolled(self, obj):
        request = self.context.get('request')

        if UserCourseEnrollment.objects.filter(user=request.user, course=obj, is_active=True).exists():
            return True
        
        return False
    
    def get_enrollment_count(self, obj):
        return obj.enrollment_count()
    
    def get_review_count(self, obj):
        return obj.review_count()


class CourseContentSerializer(serializers.ModelSerializer):

    course = serializers.SlugRelatedField(read_only=True, slug_field='slug')


    class Meta:
        model = CourseContent
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'course')

    
    def create(self, validated_data):

        course_slug = validated_data.pop('course_slug', None)
        if course_slug is not None:
            try:
                course = Course.objects.get(slug=course_slug)
            except Course.DoesNotExist:
                raise serializers.ValidationError({'course_slug': 'The course_slug is not founded.'})
        else:
            raise serializers.ValidationError({'course_slug': 'The course is needed.'})
        
        
        query = CourseFaq.objects.create(course=course, **validated_data)

        query.save()

        return query
    

    def update(self, instance, validated_data):
        instance.order = validated_data.get('order', instance.order)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.attachments = validated_data.get('attachments', instance.attachments)

        instance.save()

        return instance


class CourseFaqSerializer(serializers.ModelSerializer):

    course = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = CourseFaq
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'course')


    def create(self, validated_data):

        course_slug = validated_data.pop('course_slug', None)
        if course_slug is not None:
            try:
                course = Course.objects.get(slug=course_slug)
            except Course.DoesNotExist:
                raise serializers.ValidationError({'course_slug': 'The course_slug is not founded.'})
        else:
            raise serializers.ValidationError({'course_slug': 'The course is needed.'})
        
        question = validated_data.pop('question', None)
        if question is None:
            raise serializers.ValidationError({'question': 'question is needed.'})
        
        answer = validated_data.pop('answer', None)
        if answer is None:
            raise serializers.ValidationError({'answer': 'answer is needed.'})
        
        query = CourseFaq.objects.create(
            question=question,
            course=course,
            answer=answer
        )

        query.save()

        return query
    

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.answer = validated_data.get('answer', instance.answer)

        instance.save()

        return instance



class CourseChapterSerializer(serializers.ModelSerializer):

    course_slug = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = CourseChapter
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'course', 'duration')

    
    def create(self, validated_data):
        
        course_slug = validated_data.pop('course_slug', None)
        if course_slug is not None:
            try:
                course = Course.objects.get(slug=course_slug)
            except Course.DoesNotExist:
                raise serializers.ValidationError({'course_slug': 'The course_slug is not founded.'})
        else:
            raise serializers.ValidationError({'course_slug': 'The course is needed.'})
        
        query = CourseChapter.objects.create(course=course, **validated_data)

        query.save()

        return query
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.order = validated_data.get('order', instance.order)

        instance.save()

        return instance
        


class CourseSessionSerializer(serializers.ModelSerializer):

    chapter_id = serializers.CharField(write_only=True, required=False)

    is_active = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    file_link = serializers.SerializerMethodField()
    resources = serializers.SerializerMethodField()

    class Meta:
        model = CourseSession
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'chapter')


    def create(self, validated_data):
        
        chapter_id = validated_data.pop('chapter_id', None)
        if chapter_id is not None:
            try:
                chapter = CourseChapter.objects.get(id=chapter_id)
            except CourseChapter.DoesNotExist:
                raise serializers.ValidationError({'chapter_id': 'The chapter is not founded.'})
        else:
            raise serializers.ValidationError({'chapter_id': 'The chapter_id is needed.'})
        
        duration = validated_data.pop('duration', None)
        if duration is None:
            raise serializers.ValidationError({'duration': 'duration is needed.'})
        
        video = validated_data.pop('video', None)
        if video is None:
            raise serializers.ValidationError({'video': 'video is needed.'})
        
        is_paid = validated_data.pop('is_paid', None)
        if is_paid is None:
            raise serializers.ValidationError({'is_paid': 'is_paid is needed.'})
        
        query = CourseChapter.objects.create(
            chapter=chapter
        )

        query.save()

        return query
    
    
    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.order = validated_data.get('order', instance.order)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.description = validated_data.get('description', instance.description)

        instance.video = validated_data.get('video', instance.video)
        instance.file_link = validated_data.get('file_link', instance.file_link)
        instance.resources = validated_data.get('resources', instance.resources)

        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.is_preview = validated_data.get('is_preview', instance.is_preview)

        instance.save()

        return instance
    
    def get_is_active(self, obj):
        request = self.context.get('request')

        if not obj.is_paid:
            return True

        return UserCourseEnrollment.objects.filter(user=request.user, course=obj.chapter.course, is_active=True).exists()

    def get_video(self, obj):
        return obj.video if self.get_is_active(obj) else None

    def get_file_link(self, obj):
        return obj.file_link if self.get_is_active(obj) else None

    def get_resources(self, obj):
        return obj.resources if self.get_is_active(obj) else None




class CommentSerializer(serializers.ModelSerializer):

    course_slug = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'likes', 'course')

    
    def create(self, validated_data):

        request = self.context.get('request')
        
        course_slug = validated_data.pop('course_slug', None)
        if course_slug is not None:
            try:
                course = Course.objects.get(slug=course_slug)
            except Course.DoesNotExist:
                raise serializers.ValidationError({'course_slug': 'The course_slug is not founded.'})
        else:
            raise serializers.ValidationError({'course_slug': 'The course is needed.'})

        content = validated_data.pop('content', None)
        if content is None:
            raise serializers.ValidationError({'content': 'content is needed.'})
        
        query = Comment.objects.create(
            user=request.user,
            course=course,
            content=content
        )

        query.save()

        return query
    

    def update(self, instance, validated_data):

        request = self.context.get('request')

        if request.user.is_staff:
            instance.is_active = validated_data.get('is_active', instance.is_active)
            instance.popular_comment = validated_data.get('popular_comment', instance.popular_comment)

        instance.content = validated_data.get('content', instance.content)

        instance.save()

        return instance
    



class CommentReplySerializer(serializers.ModelSerializer):


    comment_id = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CommentReply
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user', 'comment')


    def create(self, validated_data):

        request = self.context.get('request')
        
        comment_id = validated_data.pop('comment_id', None)
        if comment_id is not None:
            try:
                course = Course.objects.get(slug=comment_id)
            except Course.DoesNotExist:
                raise serializers.ValidationError({'comment_id': 'The comment_id is not founded.'})
        else:
            raise serializers.ValidationError({'comment_id': 'The comment is needed.'})

        content = validated_data.pop('content', None)
        if content is None:
            raise serializers.ValidationError({'content': 'content is needed.'})
        
        query = Comment.objects.create(
            user=request.user,
            course=course,
            content=content
        )

        query.save()

        return query
    

    def update(self, instance, validated_data):

        instance.content = validated_data.get('content', instance.content)

        instance.save()

        return instance