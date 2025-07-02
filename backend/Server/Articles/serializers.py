from rest_framework import serializers
from .models import MainCategory, SubCategory, Tag, Author, ArticleContent



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



class AuthorSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Author
        fields = [
            'user_username',
            'full_name',
            'bio',
            'profile_picture',
            'created_at',
            'updated_at',
        ]
        
    def create(self, validated_data):
        return Author.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        
        return instance
    
    
class ArticleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleContent
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
        return ArticleContent.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.link = validated_data.get('link', instance.link)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        
        return instance
