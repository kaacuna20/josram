# Generated by Django 5.0.4 on 2024-05-01 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0005_characteristicsclothes_remove_clothes_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characteristicsclothes',
            name='color',
        ),
        migrations.AddField(
            model_name='imageclothes',
            name='color',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
