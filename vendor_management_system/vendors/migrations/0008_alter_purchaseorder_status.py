# Generated by Django 5.0.4 on 2024-05-04 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_alter_vendor_contact_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=50),
        ),
    ]
