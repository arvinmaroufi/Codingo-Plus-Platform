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
    