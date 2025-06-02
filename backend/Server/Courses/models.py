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
    

# Course model representing an individual course
class Course(models.Model):
    class CourseStatusChoices(models.TextChoices):
        COMPLETED = 'C', 'تکمیل شده'
        IN_PROGRESS = 'I', 'درحال برگزاری'
        STARTING_SOON = 'S', 'شروع به زودی'

    class CoursePaymentStatusChoices(models.TextChoices):
        FREE = 'F', 'رایگان'
        PREMIUM = 'P', 'پولی'

    class CourseLevelStatusChoices(models.TextChoices):
        INTRODUCTORY = 'IN', 'مقدماتی'
        ADVANCED = 'AD', 'پیشرفته'
        INTRODUCTORY_ADVANCED = 'IA', 'مقدماتی تا پیشرفته'
        
    class PublishStatusChoices(models.TextChoices):
        DRAFT = 'DR', 'پیش نویس شود'
        PUBLISHED = 'PD', 'منتشر شود'
    
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مدرس دوره')  # Reference to User model (teacher)
    category = models.ManyToManyField(SubCategory, related_name='courses', verbose_name='دسته بندی')  # Many-to-many relationship with subcategories
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان دوره')  # Course title
    slug = models.SlugField(max_length=200, unique=True, verbose_name='نامک')  # SEO slug
    description = RichTextUploadingField(verbose_name='توضیحات دوره')  # Rich text description
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان دوره')  # Course duration
    price = models.IntegerField(blank=True, null=True, verbose_name='قیمت دوره')  # Course price
    master_note = models.CharField(max_length=200, null=True, blank=True, verbose_name="یادداشت مدرس")  # Instructor note
    payment_status = models.CharField(choices=CoursePaymentStatusChoices.choices, max_length=10, default=CoursePaymentStatusChoices.PREMIUM, verbose_name='آیا دوره پولی است یا رایگان؟')  # Free or premium course
    poster = models.ImageField(upload_to="Courses/posters/", blank=True, null=True, verbose_name='پوستر دوره')  # Course poster image
    banner = models.ImageField(upload_to="Courses/banners/", blank=True, null=True, verbose_name='بنر دوره')  # Course banner
    level_status = models.CharField(choices=CourseLevelStatusChoices.choices, max_length=30, default=CourseLevelStatusChoices.INTRODUCTORY, verbose_name='سطح دوره')  # Course level
    course_status = models.CharField(choices=CourseStatusChoices.choices, max_length=20, default=CourseStatusChoices.STARTING_SOON, verbose_name='وضعیت دوره')  # Course status
    status = models.CharField(choices=PublishStatusChoices.choices, max_length=10, default=PublishStatusChoices.DRAFT, verbose_name='وضعیت')  # Publish status
    is_recommended = models.BooleanField(default=False, verbose_name='آیا دوره، پیشنهادی است؟')  # Recommended flag
    views = models.IntegerField(default=0, verbose_name='بازدید ها')  # Course views
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Update timestamp

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'

    def formatted_duration(self):
        """Formats duration into hours, minutes, and seconds"""
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02}"

    def __str__(self):
        return self.title  # String representation of the course
    

# Course content model for storing additional resources (images, videos, etc.)
class CourseContent(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='عنوان')  # Optional title for content
    content = RichTextUploadingField(blank=True, null=True, verbose_name='توضیحات')  # Rich text field for detailed content
    image = models.ImageField(upload_to="Courses/content/images/", null=True, blank=True, verbose_name='تصویر')  # Optional image for content
    video = models.FileField(upload_to="Courses/Content/videos/", null=True, blank=True, verbose_name='ویدیو')  # Optional video file
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Timestamp when updated

    class Meta:
        verbose_name = "محتوای دوره"
        verbose_name_plural = "محتوا های دوره ها"

    def __str__(self):
        return self.title if self.title else "Course Content"  # String representation with a fallback


# FAQ model for frequently asked questions related to a course
class CourseFaq(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره مربوطه')  # Links FAQ to a specific course
    question = models.CharField(max_length=100, verbose_name='عنوان سوال')  # Stores the question text
    answer = models.TextField(verbose_name='جواب سوال')  # Stores the answer text
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Timestamp when updated

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'

    def __str__(self):
        return self.question  # String representation of the FAQ


# Course chapter model organizing course content into structured sections
class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره مربوطه')  # Link to the parent course
    title = models.CharField(max_length=150, unique=True, verbose_name='عنوان فصل')  # Unique title for the chapter
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان')  # Duration of the chapter
    order = models.PositiveIntegerField(verbose_name='ترتیب فصل')  # Ordering index for chapters
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Timestamp when updated

    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل ها'
        ordering = ['order']  # Changed to ascending order for better organization

    def __str__(self):
        return f'{self.title} - {self.course.title}'  # String representation of the chapter


# Course session model for storing individual lesson videos and related resources
class CourseSession(models.Model):
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, verbose_name='فصل مربوطه')  # Link to chapter
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان ویدیو')  # Unique video title
    video_link = models.FileField(upload_to='Courses/Sessions/video', verbose_name='ویدیو')  # Video file
    file_link = models.URLField(max_length=500, null=True, blank=True, verbose_name='لینک فایل')  # Optional file link
    order = models.PositiveIntegerField(verbose_name='ترتیب ویدیو')  # Ordering index for sessions
    is_paid = models.BooleanField(default=False, verbose_name='پولیه؟')  # Indicates if the session requires payment
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان ویدیو')  # Duration of the session
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # Timestamp when updated

    class Meta:
        verbose_name = 'جلسه'
        verbose_name_plural = 'جلسات'
        ordering = ['order']  # Ensuring ascending order

    def formatted_duration(self):
        """Formats duration into hours, minutes, and seconds"""
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02}"

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"  # String representation of the session


# Comment model for storing user feedback on courses
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name='دوره مربوطه')  # Link to a course
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')  # Link to the user who commented
    content = models.TextField(verbose_name='نظر')  # Comment text
    popular_comment = models.BooleanField(default=False, verbose_name='آیا نظر به نظرات محبوب اضافه شود؟')  # Marks comment as popular
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return self.content[:50]  # Increased preview length for better readability


# Reply model for storing responses to comments
class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name='نظر مربوطه')  # Link to original comment
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')  # User replying
    content = models.TextField(verbose_name='نظر')  # Reply text
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # Timestamp when created
    
    class Meta:
        verbose_name = 'ریپلای'
        verbose_name_plural = 'ریپلای ها'

    def __str__(self):
        return self.content[:50]  # Consistent preview length

