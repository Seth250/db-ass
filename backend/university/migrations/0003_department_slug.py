# Generated by Django 3.0.7 on 2021-05-09 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20210509_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=75, unique=True),
        ),
    ]
