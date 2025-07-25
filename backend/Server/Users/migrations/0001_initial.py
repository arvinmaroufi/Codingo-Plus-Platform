# Generated by Django 5.2.1 on 2025-07-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_type', models.CharField(choices=[('TE', 'آموزگار'), ('ST', 'دانش آموز'), ('SU', 'پشتیبان'), ('AD', 'مدیر')], max_length=2, verbose_name='نوع کاربر')),
                ('status', models.CharField(choices=[('ACT', 'فعال'), ('SUS', 'تعلیق شده')], default='ACT', max_length=3, verbose_name='وضعیت حساب کاربری')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('username', models.CharField(max_length=40, unique=True, verbose_name='نام کاربری')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام و نام خانوادگی')),
                ('joined_date', models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به\u200cروزرسانی')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='مدیر')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['joined_date'],
            },
        ),
    ]
