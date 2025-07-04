from django.db import models


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
        upload_to='Books/MainCategory_icons/',
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
        related_name='books_subcategories',
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
        upload_to='Books/SubCategory_icons/',
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
