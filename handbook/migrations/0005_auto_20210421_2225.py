# Generated by Django 3.1.7 on 2021-04-21 19:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handbook', '0004_auto_20210421_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), size=None),
        ),
        migrations.AlterField(
            model_name='history',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), size=None),
        ),
    ]
