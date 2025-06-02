from django.db import models
from Users.models import User  # Importing the User model from the Users app
from ckeditor_uploader.fields import RichTextUploadingField  # Rich text editor for descriptions
from datetime import timedelta  # Used for duration fields

# Main category model for organizing courses
class MainCategory(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')  # Unique title for the category
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')  # Slug for SEO-friendly URLs
    icon = models.FileField(upload_to='SubCategory_icons/')  # Category icon image
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Timestamp when updated

    class Meta:
        verbose_name = 'دسته بندی والد'
        verbose_name_plural = 'دسته بندی های والد'

    def __str__(self):
        return self.title  # String representation of the category
    

# Sub-category model linked to a main category
class SubCategory(models.Model):
    parent = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories', verbose_name='دسته بندی والد')  # Establish relationship with the main category
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')  # Unique sub-category title
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')  # SEO slug
    icon = models.FileField(upload_to='SubCategory_icons/')  # Sub-category icon
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')  # Timestamp when updated

    class Meta:
        verbose_name = 'زیر دسته بندی'
        verbose_name_plural = 'زیر دسته بندی ها'

    def __str__(self):
        return self.title  # String representation of the sub-category
    
