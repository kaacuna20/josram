# Generated by Django 5.0.4 on 2024-05-01 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0003_clothes_name_alter_clothes_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='description',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
