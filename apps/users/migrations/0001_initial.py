# Generated by Django 2.2 on 2020-04-06 15:31

import core.utils.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=16, unique=True)),
                ('avatar', models.ImageField(blank=True, upload_to=core.utils.utils.get_file_path)),
                ('device_id', models.CharField(editable=False, max_length=200, null=True)),
                ('phone_number_confirmation_token', models.CharField(editable=False, max_length=12, null=True)),
                ('phone_number_valid_date', models.DateTimeField(blank=True, null=True)),
                ('reset_password_token', models.CharField(editable=False, max_length=12, null=True)),
                ('reset_password_valid_date', models.DateTimeField(blank=True, null=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_method', models.CharField(choices=[('sms', 'sms notification'), ('app', 'Application Notification'), ('bh', 'Both Types')], default='app', max_length=3)),
                ('show_phone_number', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.CharField(max_length=60, unique=True)),
                ('color', models.CharField(blank=True, max_length=15, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('car_model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.CarModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='car',
            index=models.Index(fields=['car_number', 'user'], name='users_car_car_num_4d10eb_idx'),
        ),
    ]
