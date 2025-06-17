from rest_framework import serializers
from .models import Blog, SubCategory, BlogContent, MainCategory, Tag



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
    


class BlogContentSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogContent blocks.
    This serializer is used to represent the extra content segments for a detailed blog view.
    """
    class Meta:
        model = BlogContent
        fields = [
            'id',         # Auto-generated primary key
            'title',      # Optional title for the content block
            'content',    # Rich text content
            'image',      # Optional image
            'video',      # Optional video URL
            'link',       # Optional associated link
            'order',      # Display order for the block
        ]


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blog model.
    
    Extra Fields:
    - sub_category_slug (write-only): Used for passing in the slug of the subcategory for lookup.
    - contents (nested): Accepts a list of associated blog content blocks.
    """
    # Write-only field to allow passing of the subcategory's slug during writes
    sub_category_slug = serializers.CharField(write_only=True)
    # Nested serializer for blog content blocks
    contents = BlogContentSerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Blog
        # Including read-only fields such as timestamps and automatically computed fields
        fields = [
            'id',
            'author',            # Automatically populated from request (read-only)
            'sub_category',      # Read-only view of the SubCategory relation (uses its __str__ or can be nested if desired)
            'sub_category_slug', # Write-only field used to look up the actual subcategory
            'tags',
            'title',
            'slug',
            'description',
            'poster',
            'banner',
            'status',
            'views',
            'published_at',
            'created_at',
            'updated_at',
            'contents',          # Nested content blocks
        ]
        read_only_fields = ['author', 'status', 'views', 'published_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user

        # Pop off sub_category_slug from validated_data for lookup
        sub_category_slug = validated_data.pop('sub_category_slug', None)
        if not sub_category_slug:
            raise serializers.ValidationError({"sub_category_slug": "this field is required for creating."})
        try:
            sub_category = SubCategory.objects.get(slug=sub_category_slug)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({"sub_category_slug": "This data doesn't match."})
        
        # Prevent users from setting the status while creating a new blog
        if 'status' in validated_data:
            raise serializers.ValidationError({"status": "You can't set the status while creating new blog"})
        
        # Create the blog instance with the provided data
        blog = Blog.objects.create(
            author=author,
            sub_category=sub_category,
            **validated_data
        )
        
        return blog
    
    

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Allow update only if the current user is the author or staff
        if user != instance.author and not user.is_staff:
            raise serializers.ValidationError({"error": "You don't have access to update."})
        
        # Allow staff to update the blog's status
        if user.is_staff and 'status' in validated_data:
            instance.status = validated_data.get('status', instance.status)
        
        # Update the subcategory if provided using its slug
        sub_category_slug = validated_data.pop('sub_category_slug', None)
        if sub_category_slug:
            try:
                sub_category = SubCategory.objects.get(slug=sub_category_slug)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({"sub_category_slug": "This data doesn't match."})
            instance.sub_category = sub_category

        # Update standard fields
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.banner = validated_data.get('banner', instance.banner)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.save()

        
        return instance
