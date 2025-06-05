from django.db import models
from Users.models import User  # Importing the User model from the Users app
from ckeditor_uploader.fields import RichTextUploadingField  # Rich text editor for descriptions


class MainCategory(models.Model):
    """Represents main categories for blog posts."""
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')  # Category title, ensuring uniqueness
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')  # URL-friendly identifier
    icon = models.FileField(upload_to='Blogs/MainCategory_icons/')  # Category icon
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp for when the category was created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Automatically updates when modified

    class Meta:
        verbose_name = 'دسته بندی والد'
        verbose_name_plural = 'دسته بندی های والد'

    def __str__(self):
        return self.title
    

class SubCategory(models.Model):
    """Represents subcategories under a main category."""
    parent = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories', verbose_name='دسته بندی والد')  # Links to a main category
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')  # Subcategory title, ensuring uniqueness
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')  # URL-friendly identifier
    icon = models.FileField(upload_to='Blogs/SubCategory_icons/')  # Subcategory icon
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'زیر دسته بندی'
        verbose_name_plural = 'زیر دسته بندی ها'

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    """Represents tags that can be associated with blog posts for categorization."""
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان برچسب')  # Tag name, ensuring uniqueness
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')  # URL-friendly identifier for tags
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp for when the tag was created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Automatically updates when modified

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Represents a blog post with categories, tags, author information, and metadata."""
    class PublishStatusChoices(models.TextChoices):
        DRAFT = 'DR', 'پیش نویس شود'
        PUBLISHED = 'PD', 'منتشر شود'

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده پست')  
    category = models.ManyToManyField(SubCategory, related_name='blogs', verbose_name='دسته بندی')  
    tag = models.ManyToManyField(Tag, blank=True, null=True, related_name='tags', verbose_name='برچسب')
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان پست')  
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')  
    description = RichTextUploadingField(verbose_name='توضیحات')  # Rich text content using CKEditor
    poster = models.ImageField(upload_to="Blogs/posters/", blank=True, null=True, verbose_name='پوستر پست')  
    banner = models.ImageField(upload_to="Blogs/banners/", blank=True, null=True, verbose_name='بنر پست')  
    status = models.CharField(choices=PublishStatusChoices.choices, max_length=10, default=PublishStatusChoices.DRAFT, verbose_name='وضعیت')  
    views = models.PositiveIntegerField(default=0, verbose_name='بازدید ها')  # Using PositiveIntegerField
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')  
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')  

    class Meta:
        verbose_name = 'پست بلاگ'
        verbose_name_plural = 'پست های بلاگ'

    def __str__(self):
        return self.title
    

