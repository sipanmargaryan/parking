# Generated by Django 2.2 on 2020-03-21 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_car_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
