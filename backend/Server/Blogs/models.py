from django.db import models
from django.utils import timezone
from Users.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class MainCategory(models.Model):
    """Represents main categories for blog posts."""
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
        upload_to='Blogs/MainCategory_icons/',
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
    """Represents subcategories under a main category."""
    parent = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name='subcategories',
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
        upload_to='Blogs/SubCategory_icons/',
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
    """Represents tags for blog categorization."""
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


class Blog(models.Model):
    """Represents a blog post with a primary subcategory reference, tags, and metadata."""
    class PublishStatusChoices(models.TextChoices):
        DRAFT = 'DR', 'پیش نویس شود'
        PUBLISHED = 'PD', 'منتشر شود'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='نویسنده پست'
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='blogs',
        verbose_name='دسته بندی'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='blogs',
        verbose_name='برچسب'
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='عنوان پست'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='نامک'
    )
    # Main blog description which can be used in previews or as a detailed introduction.
    description = RichTextUploadingField(
        verbose_name='توضیحات'
    )
    poster = models.ImageField(
        upload_to="Blogs/posters/",
        blank=True,
        null=True,
        verbose_name='پوستر پست'
    )
    banner = models.ImageField(
        upload_to="Blogs/banners/",
        blank=True,
        null=True,
        verbose_name='بنر پست'
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
        verbose_name = 'پست بلاگ'
        verbose_name_plural = 'پست های بلاگ'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def publish(self):
        """Publish the blog post by updating its status and publication time."""
        self.status = Blog.PublishStatusChoices.PUBLISHED
        self.published_at = timezone.now()
        self.save()


class BlogContent(models.Model):
    """
    Represents content blocks for a detailed blog view.
    Each block can have its own title, rich text content, an optional image, 
    video URL, and an associated link.
    """
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='پست مربوطه'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='عنوان بخش'
    )
    content = RichTextUploadingField(
        blank=True,
        null=True,
        verbose_name='متن بخش'
    )
    image = models.ImageField(
        upload_to="Blogs/content_images/",
        blank=True,
        null=True,
        verbose_name='تصویر بخش'
    )
    video = models.URLField(
        blank=True,
        null=True,
        verbose_name='ویدیو بخش'
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name='لینک مرتبط'
    )
    # Order in which the content block should appear in the detailed view.
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش"
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
        verbose_name = 'بخش محتوا'
        verbose_name_plural = 'بخش‌های محتوا'
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else f"محتوای بخش {self.order}"


class Comment(models.Model):
    """Represents user comments on a blog post."""
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='blog_comments',
        verbose_name='پست مربوطه'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments',
        verbose_name='کاربر'
    )
    content = models.TextField(
        verbose_name='نظر'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    approved = models.BooleanField(
        default=False,
        verbose_name='تایید شده'
    )

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50]


class CommentReply(models.Model):
    """Represents replies to user comments."""
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comments_replies',
        verbose_name='نظر مربوطه'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comment_replies',
        verbose_name='کاربر'
    )
    content = models.TextField(
        verbose_name='نظر'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    approved = models.BooleanField(
        default=False,
        verbose_name='تایید شده'
    )

    class Meta:
        verbose_name = 'ریپلای'
        verbose_name_plural = 'ریپلای ها'
        ordering = ['created_at']

    def __str__(self):
        return self.content[:50]
