# Generated by Django 5.2.1 on 2025-06-26 03:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0013_tag_alter_commentreply_options_alter_course_options_and_more'),
        ('Tickets', '0006_coursedepartment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='موضوع')),
                ('priority', models.CharField(choices=[('LW', 'کم'), ('ME', 'متوسط'), ('HG', 'بالا'), ('UR', 'اضطراری')], default='LW', max_length=10, verbose_name='اولویت')),
                ('status', models.CharField(choices=[('NW', 'جدید'), ('AD', 'پاسخ داده شده'), ('IN', 'درحال بررسی'), ('CL', 'بسته شده')], default='NW', max_length=10, verbose_name='وضعیت')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('closed_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ بسته شدن')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_tickets', to='Courses.course', verbose_name='دوره مرتبط')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tickets.coursedepartment', verbose_name='دپارتمان دوره')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_tickets', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تیکت دوره',
                'verbose_name_plural': 'تیکت\u200c های دوره',
                'ordering': ['-created_at'],
            },
        ),
    ]
