# Generated by Django 3.1.7 on 2021-04-11 13:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handbook', '0002_auto_20210404_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), size=None),
        ),
    ]
