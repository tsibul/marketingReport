# Generated by Django 4.2.4 on 2024-02-07 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0005_alter_customer_frigat_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='importcustomers',
            name='import_date',
            field=models.DateField(default=datetime.date(2024, 1, 31)),
        ),
    ]
