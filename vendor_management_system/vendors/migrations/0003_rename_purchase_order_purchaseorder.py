# Generated by Django 5.0.4 on 2024-04-30 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_alter_purchase_order_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Purchase_Order',
            new_name='PurchaseOrder',
        ),
    ]
