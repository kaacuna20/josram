# Generated by Django 5.0.4 on 2024-05-02 00:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0010_remove_imageclothes_sizes_imageclothes_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothes',
            name='images',
        ),
        migrations.RemoveField(
            model_name='imageclothes',
            name='sizes',
        ),
        migrations.AddField(
            model_name='imageclothes',
            name='clothes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Colors', to='clothes.clothes'),
        ),
        migrations.AddField(
            model_name='sizeclothes',
            name='color_clothe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='clothes.imageclothes'),
        ),
    ]
