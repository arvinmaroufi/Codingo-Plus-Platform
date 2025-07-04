# Generated by Django 5.2.1 on 2025-07-04 06:01

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0005_rename_books_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان بخش')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='متن بخش')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Books/content_images/', verbose_name='تصویر بخش')),
                ('video', models.URLField(blank=True, null=True, verbose_name='ویدیو بخش')),
                ('link', models.URLField(blank=True, null=True, verbose_name='لینک مرتبط')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='Books.book', verbose_name='کتاب مربوطه')),
            ],
            options={
                'verbose_name': 'بخش محتوا',
                'verbose_name_plural': 'بخش\u200cهای محتوا',
                'ordering': ['order'],
            },
        ),
    ]
