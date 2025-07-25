# Generated by Django 5.2.1 on 2025-07-17 07:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Otps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('purchased_on', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User course enrollment',
                'verbose_name_plural': 'Users courses enrollments',
            },
        ),
        migrations.CreateModel(
            name='AccountResetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('otp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_password', to='Otps.onetimepassword')),
            ],
            options={
                'verbose_name': 'Account reset password',
                'verbose_name_plural': 'Accounts reset passwords',
            },
        ),
    ]
