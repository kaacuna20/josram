# Generated by Django 5.0.4 on 2024-05-28 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_directpayment_date_order_created'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DirectPayment',
            new_name='DirectPayments',
        ),
    ]
