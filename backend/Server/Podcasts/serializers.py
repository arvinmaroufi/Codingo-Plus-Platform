from rest_framework import serializers
from .models import MainCategory, SubCategory, Tag, PodcastContent, Podcast, CommentReply, Comment



class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = [
            'title',
            'slug',
            'icon',
            'description',
            'created_at',
            'updated_at',
        ]
        
    
    def create(self, validated_data):
        return MainCategory.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        return instance


class SubCategorySerializer(serializers.ModelSerializer):
    main_category_slug = serializers.CharField(write_only=True)
    
    class Meta:
        model = SubCategory
        fields = [
            'title',
            'slug',
            'icon',
            'description',
            'created_at',
            'updated_at',
        ]
        
    
    def create(self, validated_data):
        
        main_category_slug = validated_data.pop('main_category_slug', None)
        if not main_category_slug:
            raise serializers.ValidationError({"main_category_slug": "this field is required for creating."})
        try:
            main_category = MainCategory.objects.get(slug=main_category_slug)
        except MainCategory.DoesNotExist:
            raise serializers.ValidationError({"main_category_slug": "This data doesn't match."})
        
        sub_category = SubCategory.objects.create(
            main_category=main_category,
            **validated_data
        )
        
        sub_category.save()
        
        return sub_category
    
    def update(self, instance, validated_data):
        
        main_category_slug = validated_data.pop('main_category_slug', None)
        if main_category_slug:
            try:
                main_category = MainCategory.objects.get(slug=main_category_slug)
            except MainCategory.DoesNotExist:
                raise serializers.ValidationError({"main_category_slug": "This data doesn't match."})
            instance.main_category = main_category
            
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'title',
            'slug',
            'created_at',
            'updated_at',
        ]
        
    
    def create(self, validated_data):
        return Tag.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        
        return instance


class PodcastContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastContent
        fields = [
            'id',
            'title',
            'content',
            'image',
            'video',
            'link',
            'order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class PodcastSerializer(serializers.ModelSerializer):
    sub_category_slug = serializers.CharField(write_only=True)
    contents = PodcastContentSerializer(many=True, required=False, read_only=True)

    file = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    
    class Meta:
        model = Podcast
        fields = [
            'id',
            'title',
            'description',
            'presenter',
            'sub_category',
            'sub_category_slug',
            'tags',
            'image',
            'file',
            'audio',
            'video',
            'payment_status',
            'type_status',
            'language',
            'created_at',
            'updated_at',
            'contents',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        sub_category_slug = validated_data.pop('sub_category_slug', None)
        if not sub_category_slug:
            raise serializers.ValidationError({"sub_category_slug": "This field is required for creating."})
        
        try:
            sub_category = SubCategory.objects.get(slug=sub_category_slug)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({"sub_category_slug": "SubCategory with this slug doesn't exist."})
        
        podcast = Podcast.objects.create(sub_category=sub_category, **validated_data)
        
        return podcast

    def update(self, instance, validated_data):
        sub_category_slug = validated_data.pop('sub_category_slug', None)
        if sub_category_slug:
            try:
                sub_category = SubCategory.objects.get(slug=sub_category_slug)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({"sub_category_slug": "SubCategory with this slug doesn't exist."})
            instance.sub_category = sub_category

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.presenter = validated_data.get('presenter', instance.presenter)
        instance.image = validated_data.get('image', instance.image)
        instance.file = validated_data.get('file', instance.file)
        instance.audio = validated_data.get('audio', instance.audio)
        instance.video = validated_data.get('video', instance.video)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.type_status = validated_data.get('type_status', instance.type_status)
        instance.language = validated_data.get('language', instance.language)
        instance.save()

        return instance
    

    def get_file(self, obj):
        request = self.context.get('request')

        user = request.user

        if obj.payment_status == "F":
            return obj.file
        
        try:
            if user.user_subscription.is_active():
                return obj.file
        except:
            pass

        return None
    
    def get_audio(self, obj):
        request = self.context.get('request')

        user = request.user

        if obj.payment_status == "F":
            return obj.audio

        try:
            if user.user_subscription.is_active():
                return obj.audio
        except:
            pass
        
        return None
    
    def get_video(self, obj):
        request = self.context.get('request')

        user = request.user

        if obj.payment_status == "F":
            return obj.video

        try:
            if user.user_subscription.is_active():
                return obj.video
        except:
            pass
        
        return None


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'approved',
        ]
        read_only_fields = ['user', 'created_at']
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return CommentReply.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.save()
        
        return instance


class CommentSerializer(serializers.ModelSerializer):
    
    replies = CommentReplySerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'blog',
            'user',
            'content',
            'created_at',
            'approved',
            'replies',
        ]
        read_only_fields = ['user', 'created_at']
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.save()
        
        return instance
