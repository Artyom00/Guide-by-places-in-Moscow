# Generated by Django 3.1.7 on 2021-04-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handbook', '0008_auto_20210428_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='subway',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
