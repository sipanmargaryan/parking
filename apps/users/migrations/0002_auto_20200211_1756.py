# Generated by Django 2.2 on 2020-02-11 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='model',
            new_name='car_model',
        ),
    ]
