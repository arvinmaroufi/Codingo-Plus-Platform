from rest_framework import serializers
from .models import MainCategory, SubCategory, Tag, BookContent, Book, CommentReply, Comment



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


class BookContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookContent
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
        
    def create(self, validated_data):
        return BookContent.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.link = validated_data.get('link', instance.link)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        
        return instance


class BookSerializer(serializers.ModelSerializer):
    sub_category_slug = serializers.CharField(write_only=True)
    tags_slugs = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    contents = BookContentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id',
            'sub_category_slug',
            'tags_slugs',
            'title',
            'slug',
            'description',
            'author',
            'image',
            'file',
            'payment_status',
            'language',
            'published_at',
            'created_at',
            'updated_at',
            'contents',
        ]
        
    def create(self, validated_data):
        tags_slugs = validated_data.pop('tags_slugs', [])
        sub_category_slug = validated_data.pop('sub_category_slug')
        
        try:
            sub_category = SubCategory.objects.get(slug=sub_category_slug)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({"sub_category_slug": "SubCategory does not exist."})
            
        book = Book.objects.create(
            sub_category=sub_category,
            **validated_data
        )
        
        if tags_slugs:
            tags = Tag.objects.filter(slug__in=tags_slugs)
            book.tags.set(tags)
            
        return book
    
    def update(self, instance, validated_data):
        tags_slugs = validated_data.pop('tags_slugs', None)
        sub_category_slug = validated_data.pop('sub_category_slug', None)
        
        if sub_category_slug:
            try:
                sub_category = SubCategory.objects.get(slug=sub_category_slug)
                instance.sub_category = sub_category
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({"sub_category_slug": "SubCategory does not exist."})
                
        if tags_slugs is not None:
            tags = Tag.objects.filter(slug__in=tags_slugs)
            instance.tags.set(tags)
            
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.image = validated_data.get('image', instance.image)
        instance.file = validated_data.get('file', instance.file)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        
        return instance


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
