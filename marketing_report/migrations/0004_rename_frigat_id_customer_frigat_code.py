# Generated by Django 4.2.4 on 2024-02-05 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0003_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='frigat_id',
            new_name='frigat_code',
        ),
    ]