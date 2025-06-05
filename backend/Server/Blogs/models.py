from django.db import models


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
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'زیر دسته بندی'
        verbose_name_plural = 'زیر دسته بندی ها'

    def __str__(self):
        return self.title
    

