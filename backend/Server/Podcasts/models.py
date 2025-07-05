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
        upload_to='Podcasts/MainCategory_icons/',
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
        related_name='podcasts_subcategories',
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
        upload_to='Podcasts/SubCategory_icons/',
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


class Podcast(models.Model):
    
    class PaymentStatusChoices(models.TextChoices):
        FREE = 'F', 'رایگان'
        SUBSCRIPTION = 'S', 'اشتراکی'
    
    class TypeStatusChoices(models.TextChoices):
        AUDIO = 'A', 'ضوتی'
        VIDEO = 'V', 'ویدیو'
        BOTH = 'B', 'هردو'
        
    class LanguageChoices(models.TextChoices):
        FA = 'FA', 'فارسی'
        EN = 'EN', 'انگلیسی'
        
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='عنوان پادکست'
    )
    description = models.TextField(
        verbose_name='توضیحات'
    )
    presenter = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='گوینده پادکست'
    )
    image = models.ImageField(
        upload_to="Podcasts/images/",
        blank=True,
        null=True,
        verbose_name='تصویر پادکست'
    )
    file = models.FileField(
        upload_to='Podcasts/files/',
        blank=True,
        null=True,
        verbose_name='فایل'
    )
    audio = models.FileField(
        upload_to='Podcasts/audios/',
        blank=True,
        null=True,
        verbose_name='فایل صوتی'
    )
    video = models.FileField(
        upload_to='Podcasts/videos/',
        blank=True,
        null=True,
        verbose_name='ویدیو ها'
    )
    payment_status = models.CharField(
        max_length=1,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.SUBSCRIPTION
    )
    type_status = models.CharField(
        max_length=1,
        choices=TypeStatusChoices.choices,
        default=TypeStatusChoices.AUDIO
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.FA
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
        verbose_name = 'پادکست'
        verbose_name_plural = 'پادکست ها'

    def __str__(self):
        return self.title
