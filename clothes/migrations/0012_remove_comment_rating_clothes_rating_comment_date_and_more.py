# Generated by Django 5.0.4 on 2024-05-05 23:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0011_remove_clothes_images_remove_imageclothes_sizes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rating',
        ),
        migrations.AddField(
            model_name='clothes',
            name='rating',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sizeclothes',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
