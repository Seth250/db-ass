# Generated by Django 3.0.7 on 2021-05-08 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=25, verbose_name='last name'),
        ),
    ]
