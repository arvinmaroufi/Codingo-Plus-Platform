from django.db import models
from Users.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class MainCategory(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='عنوان دسته بندی'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='نامک'
    )
    icon = models.FileField(
        upload_to='Articles/MainCategory_icons/',
        verbose_name='آیکون'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )

    class Meta:
        verbose_name = 'دسته بندی والد'
        verbose_name_plural = 'دسته بندی های والد'
        ordering = ['title']

    def __str__(self):
        return self.title
    

class SubCategory(models.Model):
    parent = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name='articles_subcategories',
        verbose_name='دسته بندی والد'
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='عنوان دسته بندی'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='نامک'
    )
    icon = models.FileField(
        upload_to='Articles/SubCategory_icons/',
        verbose_name='آیکون'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )

    class Meta:
        verbose_name = 'زیر دسته بندی'
        verbose_name_plural = 'زیر دسته بندی ها'
        ordering = ['title']

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='عنوان برچسب'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='نامک'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'
        ordering = ['title']

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='کاربر'
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='نام و نام خانوادگی'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='بیو'
    )   
    profile_picture = models.ImageField(
        upload_to='Articles/Author/profile_picture/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )
    
    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسنده ها'
    
    def __str__(self):
        return self.full_name


class Article(models.Model):
    class PublishStatusChoices(models.TextChoices):
        DRAFT = 'DR', 'پیش نویس شود'
        PUBLISHED = 'PD', 'منتشر شود'

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='نویسنده مقاله'
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='دسته بندی'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        verbose_name='برچسب'
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='عنوان مقاله'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='نامک'
    )
    description = RichTextUploadingField(
        verbose_name='توضیحات'
    )
    poster = models.ImageField(
        upload_to="Articles/posters/",
        blank=True,
        null=True,
        verbose_name='پوستر مقاله'
    )
    banner = models.ImageField(
        upload_to="Articles/banners/",
        blank=True,
        null=True,
        verbose_name='بنر مقاله'
    )
    status = models.CharField(
        choices=PublishStatusChoices.choices,
        max_length=10,
        default=PublishStatusChoices.DRAFT,
        verbose_name='وضعیت'
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='بازدید ها'
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='تاریخ انتشار'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ساخت'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def publish(self):
        self.status = Article.PublishStatusChoices.PUBLISHED
        self.published_at = timezone.now()
        self.save()
