# Generated by Django 2.2 on 2020-04-06 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Country'),
        ),
    ]