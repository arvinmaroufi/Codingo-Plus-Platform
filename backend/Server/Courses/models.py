from datetime import timedelta
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from Users.models import User



# -------------------- Categories -------------------- #
class MainCategory(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')
    icon = models.FileField(upload_to='Courses/SubCategory_icons/', verbose_name='آیکون دسته بندی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات دسته بندی')
    color_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='کد رنگ (HEX)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'دسته بندی والد'
        verbose_name_plural = 'دسته بندی های والد'

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    parent = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='دسته بندی والد'
    )
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')
    icon = models.FileField(upload_to='Courses/SubCategory_icons/', verbose_name='آیکون زیر دسته بندی')
    banner = models.ImageField(
        upload_to='Courses/SubCategory_banners/',
        null=True,
        blank=True,
        verbose_name='بنر زیر دسته بندی'
    )
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات زیر دسته بندی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'زیر دسته بندی'
        verbose_name_plural = 'زیر دسته بندی ها'

    def __str__(self):
        return self.title

# -------------------- Tag -------------------- #

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='برچسب')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='نامک برچسب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'

    def __str__(self):
        return self.name

# -------------------- Course -------------------- #

class Course(models.Model):
    # ── Choice enums ──
    class Status(models.TextChoices):
        COMPLETED = 'C', 'تکمیل شده'
        IN_PROGRESS = 'I', 'درحال برگزاری'
        STARTING_SOON = 'S', 'شروع به زودی'

    class Payment(models.TextChoices):
        FREE = 'F', 'رایگان'
        PREMIUM = 'P', 'پولی'

    class Level(models.TextChoices):
        INTRO = 'IN', 'مقدمه‌ای'
        MID = 'IM', 'متوسط'
        ADV = 'AD', 'پیشرفته'
        FULL = 'IA', 'مقدماتی تا پیشرفته'

    class Publish(models.TextChoices):
        DRAFT = 'DR', 'پیش نویس'
        PUBLISHED = 'PD', 'منتشر شده'

    class Language(models.TextChoices):
        FA = 'FA', 'فارسی'
        EN = 'EN', 'انگلیسی'

    # ── Relations ──
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='categories_courses')
    tags = models.ManyToManyField('Tag', blank=True, related_name='courses')

    # ── Core fields ──
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    description = RichTextUploadingField()

    # ── Content details ──
    prerequisites = models.TextField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True, null=True)
    duration = models.DurationField(default=timedelta())

    # ── Pricing & access ──
    price = models.PositiveIntegerField(blank=True, null=True)
    payment_status = models.CharField(
        max_length=1,
        choices=Payment.choices,
        default=Payment.PREMIUM
    )

    # ── Media ──
    poster = models.ImageField(upload_to='courses/posters/', blank=True, null=True)
    banner = models.ImageField(upload_to='courses/banners/', blank=True, null=True)
    trailer = models.FileField(upload_to='courses/trailers/', blank=True, null=True)

    # ── Metadata & statuses ──
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.FA)
    level_status = models.CharField(max_length=2, choices=Level.choices, default=Level.INTRO)
    course_status = models.CharField(max_length=1, choices=Status.choices, default=Status.STARTING_SOON)
    status = models.CharField(max_length=2, choices=Publish.choices, default=Publish.DRAFT)
    has_certificate = models.BooleanField(default=False)

    # ── Engagement stats ──
    enrollment_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    is_recommended = models.BooleanField(default=False)

    # ── Timestamps ──
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def formatted_duration(self):
        """
        Return duration as "HH:MM:SS" (or "MM:SS" if under 1 hour).
        """
        total = int(self.duration.total_seconds())
        hrs, rem = divmod(total, 3600)
        mins, secs = divmod(rem, 60)
        return f"{hrs:02}:{mins:02}:{secs:02}" if hrs else f"{mins:02}:{secs:02}"


# -------------------- Course Content -------------------- #

class CourseContent(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='دوره مرتبط'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب محتوا')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='عنوان محتوا')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='توضیحات محتوا')
    image = models.ImageField(upload_to="Courses/content/images/", null=True, blank=True, verbose_name='تصویر محتوا')
    video = models.FileField(upload_to="Courses/content/videos/", null=True, blank=True, verbose_name='ویدیو محتوا')
    attachments = models.FileField(
        upload_to="Courses/content/attachments/",
        null=True,
        blank=True,
        verbose_name='فایل ضمیمه'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = "محتوای دوره"
        verbose_name_plural = "محتواهای دوره"
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else "Course Content"

# -------------------- FAQs -------------------- #

class CourseFaq(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره مربوطه')
    question = models.CharField(max_length=100, verbose_name='سوال')
    answer = models.TextField(verbose_name='پاسخ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'

    def __str__(self):
        return self.question

# -------------------- Chapters and Sessions -------------------- #

class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره مربوطه')
    title = models.CharField(max_length=150, unique=True, verbose_name='عنوان فصل')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات فصل')
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان فصل')
    order = models.PositiveIntegerField(verbose_name='ترتیب فصل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصول'
        ordering = ['order']

    def __str__(self):
        return f'{self.title} - {self.course.title}'


class CourseSession(models.Model):
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, verbose_name='فصل مربوطه')
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان جلسه')
    video = models.FileField(upload_to='Courses/sessions/videos/', verbose_name='ویدیو جلسه')
    file_link = models.URLField(max_length=500, null=True, blank=True, verbose_name='لینک فایل درسی')
    resources = models.FileField(
        upload_to='Courses/sessions/resources/',
        null=True,
        blank=True,
        verbose_name='منابع پیوست'
    )
    order = models.PositiveIntegerField(verbose_name='ترتیب جلسه')
    is_paid = models.BooleanField(default=False, verbose_name='پولی؟')
    is_preview = models.BooleanField(default=False, verbose_name='پیش‌نمایش؟')
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان جلسه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'جلسه'
        verbose_name_plural = 'جلسات'
        ordering = ['order']

    def formatted_duration(self):
        """
        Formats duration into hours, minutes, and seconds.
        """
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02}"

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"

# -------------------- Comments -------------------- #

class Comment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='دوره مربوطه'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    content = models.TextField(verbose_name='نظر')
    popular_comment = models.BooleanField(default=False, verbose_name='نظر برگزیده')
    likes = models.PositiveIntegerField(default=0, verbose_name='تعداد لایک')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return self.content[:50]


class CommentReply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='نظر مربوطه'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_comment_replies',
        verbose_name='کاربر'
    )
    content = models.TextField(verbose_name='پاسخ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ‌ها'

    def __str__(self):
        return self.content[:50]
